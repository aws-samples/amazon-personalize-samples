import pandas as pd
import pylab as pl
import numpy as np
import warnings
import traceback
import scipy.sparse as ss
import time


INTERACTIONS_REQUIRED_FIELDS = ["USER_ID", "ITEM_ID", "TIMESTAMP"]
# general
NA_RATE_THRESHOLD        = 0.1
DUP_RATE_THRESHOLD       = 0.1
REPEAT_RATE_THRESHOLD    = 0.5
COLDSTART_RATE_THRESHOLD = 0.1

# loglog warning thresholds
LOGLOG_RMSE_THRESHOLD = 5
LOGLOG_MIN_CATS       = 30
LOGLOG_HEAD_HEAVY     = -2
LOGLOG_HEAVY_TAIL     = -0.75

# metadata
CATS_FREQ_HEAD = 10

# temporal analysis
EPS_GREEDY = 0.01
TIMEDELTA_REFERENCES = [
    ('min', 60), ('hour',3600), ('day',3600*24),
    ('week',3600*24*7), ('month',3600*24*31),
    ('year',3600*24*365)]
ROLLING_HISTORY_LEN = [1, 10, 100, 1000]
TEMPORAL_FREQUENCY = ['5d', '1d', '3h']
TEMPORAL_PLOT_LIMIT = 50


def plot_loglog(val, name='', show=True):
    x = 1+np.arange(len(val))
    slope, intercept = np.polyfit(np.log10(x)[val>0], np.log10(val[val>0]), deg=1)
    full_ret = np.polyfit(np.log10(x)[val>0], np.log10(val[val>0]), deg=1, full=True)
    rmse = np.mean(full_ret[0]**2)**0.5
    fitted = 10**(intercept + slope*np.log10(x))
    pl.loglog(x, val)
    _axis = pl.axis()
    pl.loglog(x, fitted, ':')
    pl.axis(_axis)
    pl.grid()
    pl.title(name + ' loglog, %.2e * x^(%.2f), rmse=%.2f' %(10**intercept, slope, rmse))
    pl.ylabel('value threshold')
    pl.xlabel('number of examples with value <= threshold')
    if show:
        pl.show()
    return (slope, intercept, rmse)


def describe_categorical(sr, name=''):
    print("\n=== {} top {} categories ===".format(name, CATS_FREQ_HEAD))
    parts = sr.astype(str).apply(lambda x: x.split('|'))
    cats = pd.Series(np.hstack(parts.values))
    cats_freq = cats.groupby(cats).size().sort_values(ascending=False)
    print(cats_freq.head(CATS_FREQ_HEAD))

    if len(cats_freq) <= LOGLOG_MIN_CATS:
        return None

    (slope, intercept, rmse) = plot_loglog(cats_freq, name)

    if len(cats_freq) > LOGLOG_MIN_CATS and rmse < LOGLOG_RMSE_THRESHOLD:
        if slope > LOGLOG_HEAVY_TAIL:
            warnings.warn("""
            Heavy-tail {0} distributions are usually hard to learn (slope={1})!
            Consider rolling up {0} or dropping its rare values.
            """.format(name, slope))

        elif slope < LOGLOG_HEAD_HEAVY:
            warnings.warn("""
            Head-heavy {0} distributions are usually uninteresting or spammy (slope={1})!
            Consider using finer-grade {0} or thresholding its dominate values.
            """.format(name, slope))

    return (slope, intercept, rmse)


def describe_dataframe(df, name=''):
    print("\n=== Describe {} ===\n".format(name))
    print(df.describe())
    if object in df.dtypes:
        print(df.describe(include=['O']))

    summary = {}
    for cn, dtype in df.dtypes.iteritems():
        if dtype == object:
            summary_cn = describe_categorical(df[cn], cn)
            if summary_cn is not None:
                summary[cn] = summary_cn
    return summary


def _normalize_distribution(X, jitter=1e-20):
    sums = np.ravel(X.sum(axis=1))
    rows = np.split(X.data, X.indptr[1:-1])
    X_data = np.hstack([
        x/(s+jitter) for s,x in
        zip(sums, rows)
    ])
    return ss.csr_matrix(
        (X_data, X.indices, X.indptr),
        shape=X.shape)


def compute_distribution_shift(index, df_wgt, p, q, method, hist_len, freq=None, tic=0):
    """ p:target (unobserved), q:data (observed) """

    N = p.shape[1]
    p = _normalize_distribution(p)
    q = _normalize_distribution(q)

    if method.lower() in ['kl', 'kl-divergence']:
        eps_ratio = (1-EPS_GREEDY) / (EPS_GREEDY / N)
        log_p = (p * eps_ratio).log1p()
        log_q = (q * eps_ratio).log1p()
        temporal_loss = (p .multiply (log_p - log_q)).sum(axis=1)
        loss_fmt = '{:.2f}'

    elif method.lower() in ['ce', 'cross-entropy']:
        eps_ratio = (1-EPS_GREEDY) / (EPS_GREEDY / N)
        log_q = (q * eps_ratio).log1p()
        temporal_loss = -((p .multiply (log_q)).sum(axis=1) + np.log(EPS_GREEDY/N))
        loss_fmt = '{:.2f}'

    elif method.lower() in ['oov', 'out-sample items']:
        temporal_loss = 1.0 - (p .multiply (q>0)).sum(axis=1)
        loss_fmt = '{:.1%}'

    elif method.lower() in ['tv', 'total variation']:
        temporal_loss = 0.5 * abs(q - p).sum(axis=1)
        loss_fmt = '{:.1%}'

    else:
        raise NotImplementedError

    temporal_loss = pd.Series(np.ravel(temporal_loss), index=index)

    avg_loss = np.average(temporal_loss.values, weights=df_wgt.values)

    print('temporal {}, freq={}, hist_len={}, avg_loss={}, time={:.1f}s'.format(
        method, freq, hist_len, loss_fmt.format(avg_loss), time.time() - tic,
    ))
    return temporal_loss, df_wgt, avg_loss, loss_fmt


def compute_bootstrap_loss(df, freq, method):
    tic = time.time()

    df = df.join(
        df.groupby('USER_ID').apply(lambda x:np.random.rand()<0.5).to_frame('_bs'),
        on='USER_ID')

    df_cnt = df.groupby(['_bs', pd.Grouper(freq=freq), 'ITEM_ID']).size()
    df_cnt = df_cnt.to_frame('_cnt').reset_index(level=(0,2))

    index = pd.date_range(
        df_cnt.index.min(),
        df_cnt.index.max(),
        freq=freq)
    df_wgt = df.groupby(pd.Grouper(freq=freq)).size().reindex(index, fill_value=0)

    df_cnt['_i'] = np.searchsorted(index, df_cnt.index)
    df_cnt['_j'] = df_cnt['ITEM_ID'].astype('category').cat.codes
    N = len(df_cnt['ITEM_ID'].unique())

    Y, X = [ss.coo_matrix((
        df_cnt[df_cnt['_bs'] == split]['_cnt'],
        (df_cnt[df_cnt['_bs'] == split]['_i'],
         df_cnt[df_cnt['_bs'] == split]['_j'])
    ), shape=(len(index), N)).tocsr() for split in [0, 1]]

    return compute_distribution_shift(index, df_wgt, Y, X, method, 0, freq, tic)


def compute_temporal_loss(df, freq, method, hist_len):
    tic = time.time()

    df_cnt = df.groupby([pd.Grouper(freq=freq), 'ITEM_ID']).size()
    df_cnt = df_cnt.to_frame('_cnt').reset_index(level=1)

    index = pd.date_range(
        df_cnt.index.min(),
        df_cnt.index.max(),
        freq=freq)
    df_wgt = df.groupby(pd.Grouper(freq=freq)).size().reindex(index, fill_value=0)

    df_cnt['_i'] = np.searchsorted(index, df_cnt.index)
    df_cnt['_j'] = df_cnt['ITEM_ID'].astype('category').cat.codes
    N = len(df_cnt['ITEM_ID'].unique())

    # sparse data
    Y = ss.coo_matrix((
        df_cnt['_cnt'], (df_cnt['_i'], df_cnt['_j'])
    ), shape=(len(index), N)).tocsr()

    try: # binary rolling sum
        B = Y
        X = 0
        c = 1
        for p,b in enumerate(reversed('{0:b}'.format(hist_len))):
            if b == '1' and c < len(index):
                X = X + ss.vstack([ss.csr_matrix((c, N)), B[:-c]])
                c = c + 2**p
            if 2**p < len(index):
                B = B + ss.vstack([ss.csr_matrix((2**p, N)), B[:-2**p]]) # sum 0 .. 2**(p+1)-1

        assert np.allclose(X[-1:].sum(axis=0), Y[-hist_len-1:-1].sum(axis=0))

    except Exception:
        traceback.print_exc()
        warnings.warn("falling back to plain rolling sum")

        rolling = 0
        for t in range(hist_len):
            rolling = rolling + ss.eye(len(index), k=-t-1)
        X = rolling .dot( Y )

    return compute_distribution_shift(index, df_wgt, Y, X, method, hist_len, freq, tic)


def diagnose_interactions(df):
    print("\n=== Interactions table, original shape={} ===\n"
          .format(df.shape))
    df = df.copy()
    df['ITEM_ID'] = df['ITEM_ID'].astype(str)
    df['USER_ID'] = df['USER_ID'].astype(str)
    df.index = df["TIMESTAMP"].values.astype("datetime64[s]")


    na_rate = df[INTERACTIONS_REQUIRED_FIELDS].isnull().any(axis=1).mean()
    print("missing rate in fields", INTERACTIONS_REQUIRED_FIELDS, na_rate)
    if na_rate > NA_RATE_THRESHOLD:
        warnings.warn("High data missing rate for required fields ({:.1%})!".format(na_rate))
    df = df.dropna(subset=INTERACTIONS_REQUIRED_FIELDS)
    print("dropna shape", df.shape)


    dup_rate = (df.groupby(INTERACTIONS_REQUIRED_FIELDS).size() - 1.0).sum() / df.shape[0]
    print("duplication rate", dup_rate)
    if dup_rate > DUP_RATE_THRESHOLD:
        warnings.warn("""
        High duplication rate ({:.1%})!
        Only one event can be taken at the same (user,item,timestamp) index.
        """.format(dup_rate))
    df = df.drop_duplicates(subset=INTERACTIONS_REQUIRED_FIELDS)
    print("drop_duplicates shape", df.shape)


    repeat_rate = (df.groupby(["USER_ID", "ITEM_ID"]).size() - 1.0).sum() / df.shape[0]
    print("user item repeat rate", repeat_rate)
    if repeat_rate > REPEAT_RATE_THRESHOLD:
        warnings.warn("""
        High rate of repeated consumptions ({:.1%})!
        We would not do anything, but it may beneficial to
        (1) consider keeping only the last interaction between the same user-item pair,
        (2) consider if the ITEM_IDs have collisions, and/or
        (3) use high-order hierarchical models.
        """.format(repeat_rate))

    summary = describe_dataframe(df, 'interactions table')


    print("\n=== Hourly activity pattern ===")
    print(df.groupby(df.index.hour).size())

    print("\n=== Day of week activity pattern ===")
    print(df.groupby(df.index.dayofweek).size())

    plot_patterns = {
        "date": df.index.date,
        "hour": df.index.hour,
        "dayofweek": df.index.dayofweek}

    for k,v in plot_patterns.items():
        pl.plot(df.groupby(v).size(), '.-')
        pl.gcf().autofmt_xdate()
        pl.title("Activity pattern by %s" %k)
        pl.grid()
        pl.show()


    print("\n=== Temporal shift analysis ===\n")

    for freq in TEMPORAL_FREQUENCY:
        for method in ['out-sample items', 'total variation']:
            bootstrap_loss, _, avg_loss, loss_fmt = compute_bootstrap_loss(df, freq, method)
            pl.plot(bootstrap_loss.iloc[-TEMPORAL_PLOT_LIMIT:], '.--',
                        label = 'boostrap, avg={}'.format(loss_fmt.format(avg_loss)))

            for hist_len in ROLLING_HISTORY_LEN:
                temporal_loss, df_wgt, avg_loss, loss_fmt = compute_temporal_loss(df, freq, method, hist_len)

                pl.plot(temporal_loss.iloc[-TEMPORAL_PLOT_LIMIT:], '.-',
                        label = 'hist={} * {}, avg={}'.format(hist_len, freq, loss_fmt.format(avg_loss)))

            pl.gca().yaxis.set_major_formatter(pl.FuncFormatter(lambda y, _: loss_fmt.format(y)))

            pl.title('{} {} from rolling history (lower is better)'.format(freq, method))
            pl.grid()
            pl.gcf().autofmt_xdate()
            pl.legend(loc='upper left')
            pl.twinx()
            pl.plot(df_wgt.iloc[-TEMPORAL_PLOT_LIMIT:], color='grey', lw=3, ls='--', alpha=0.5)
            pl.legend(['activity density'], loc='upper right')
            pl.show()

    print("\n=== session time delta describe ===")
    df.sort_index(inplace=True)

    user_time_delta = df.groupby('USER_ID')["TIMESTAMP"].transform(pd.Series.diff).dropna()
    user_time_delta.sort_values(ascending=False, inplace=True)
    print(user_time_delta.describe())
    plot_loglog(user_time_delta, 'session time delta', show=False)
    for k,v in TIMEDELTA_REFERENCES:
        if pl.ylim()[0] < v < pl.ylim()[1]:
            pl.plot(pl.xlim(), [v,v], '--')
            pl.text(pl.xlim()[0], v, k)
    pl.show()


    user_time_span = df.groupby('USER_ID')["TIMESTAMP"].apply(lambda x:max(x)-min(x))
    user_time_span.sort_values(ascending=False, inplace=True)
    print("=== user time span describe ===")
    print(user_time_span.describe())
    plot_loglog(user_time_span, 'user time span', show=False)
    for k,v in TIMEDELTA_REFERENCES:
        if pl.ylim()[0] < v < pl.ylim()[1]:
            pl.plot(pl.xlim(), [v,v], '--')
            pl.text(pl.xlim()[0], v, k)
    pl.show()


#     date_and_item_size = df.groupby([pd.Grouper(freq='1D'), 'ITEM_ID']).size()
#     date_and_item_size = date_and_item_size.to_frame(
#         'size').reset_index('ITEM_ID').sort_values('size', ascending=False)

#     print("=== number of days when an item stays as daily top-1 ===")
#     daily_top_1s = date_and_item_size.groupby(level=0).head(
#         1).groupby('ITEM_ID').size().sort_values(ascending=False)
#     print(daily_top_1s.head(10))

#     print("=== number of days when an item stays in daily top-5 ===")
#     daily_top_5s = date_and_item_size.groupby(level=0).head(
#         5).groupby('ITEM_ID').size().sort_values(ascending=False)
#     print(daily_top_5s.head(10))


def diagnose_users(df, users):
    print("\n=== Users table, original shape={} ===\n"
          .format(users.shape))
    users = users.copy()
    users['USER_ID'] = users['USER_ID'].astype(str)
    users = users.set_index('USER_ID')

    missing_rate = 1 - df.USER_ID.astype(str).isin(set(users.index.values)).mean()
    print("Missing rate of all user meta-data", missing_rate)
    if missing_rate > NA_RATE_THRESHOLD:
        warnings.warn("High missing rate of all user meta-data ({:%})!"
                      .format(missing_rate))

    coldstart_rate = 1 - users.index.isin(set(df.USER_ID.astype(str).values)).mean()
    print("User coldstart rate", coldstart_rate)
    if coldstart_rate > COLDSTART_RATE_THRESHOLD:
        warnings.warn("High user coldstart rate ({:%})!"
                      .format(coldstart_rate))

    describe_dataframe(users)


def diagnose_items(df, items):
    print("\n=== Items table, original shape={} ===\n"
          .format(items.shape))
    items = items.copy()
    items['ITEM_ID'] = items['ITEM_ID'].astype(str)
    items = items.set_index('ITEM_ID')

    missing_rate = 1 - df.ITEM_ID.astype(str).isin(set(items.index.values)).mean()
    print("Missing rate of all item meta-data", missing_rate)
    if missing_rate > NA_RATE_THRESHOLD:
        warnings.warn("High missing rate of all item meta-data ({:%})!"
                      .format(missing_rate))

    coldstart_rate = 1 - items.index.isin(set(df.ITEM_ID.astype(str).values)).mean()
    print("Item coldstart rate", coldstart_rate)
    if coldstart_rate > NA_RATE_THRESHOLD:
        warnings.warn("High item coldstart rate ({:%})!"
                      .format(coldstart_rate))

    describe_dataframe(items)

    if 'CREATION_TIMESTAMP' in items:
        items.index = items['CREATION_TIMESTAMP'].values.astype("datetime64[s]")
        items.sort_index(inplace=True)

        pl.plot(items.groupby(items.index.date).size())
        pl.gcf().autofmt_xdate()
        pl.title("daily item creation pattern")
        pl.grid()
        pl.show()

    else:
        print("CREATION_TIMESTAMP not found in items table")


def diagnose(df, users=None, items=None):
    print("########################################")
    print("# DIAGNOSING INTERACTIONS TABLE, SAMPLE:")
    print("########################################")
    print(df.sample(min(len(df), 10)))
    diagnose_interactions(df)

    if users is not None:
        print("########################################")
        print("# DIAGNOSING USERS TABLE, SAMPLE:")
        print("########################################")
        print(users.sample(min(len(users), 10)))
        diagnose_users(df, users)
    else:
        print("########################################")
        print("# USERS TABLE NOT FOUND")
        print("########################################")

    if items is not None:
        print("########################################")
        print("# DIAGNOSING ITEMS TABLE, SAMPLE:")
        print("########################################")
        print(items.sample(min(len(items), 10)))
        diagnose_items(df, items)
    else:
        print("########################################")
        print("# ITEMS TABLE NOT FOUND")
        print("########################################")
