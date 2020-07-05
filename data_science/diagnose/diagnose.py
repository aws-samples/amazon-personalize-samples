import pandas as pd
import pylab as pl
import numpy as np
import warnings
import traceback
import scipy.sparse as ss
import time
import argparse
import os
import re
import yaml

parser = argparse.ArgumentParser(description="""
    A tool to provide dataset statistics.
    If datasets are provided, conduct the analysis.
    Otherwise, it will load the functions with the defaults provided in yaml.
    This is useful if this function is called via jupyter magic `%run script`.
    """)
parser.add_argument('--yaml', default='diagnose.yaml')
parser.add_argument('--datasets', nargs='*', help='interactions, users, items')
args, _ = parser.parse_known_args()

with open(args.yaml) as fp:
    config = yaml.safe_load(fp)


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
    pl.xlabel('number of examples with value >= threshold')
    if show:
        pl.show()
    return (slope, intercept, rmse)


def describe_categorical(sr, name=''):
    print("\n=== {} top {} categories ===".format(name, config['num_top_categories_to_show']))
    parts = sr.astype(str).apply(lambda x: x.split('|'))
    cats = pd.Series(np.hstack(parts.values))
    cats_freq = cats.groupby(cats).size().sort_values(ascending=False)
    print(cats_freq.head(config['num_top_categories_to_show']))

    if len(cats_freq) <= config['loglog_min_categories_to_show']:
        return None

    (slope, intercept, rmse) = plot_loglog(cats_freq, name)

    if len(cats_freq) > config['loglog_min_categories_to_show'] and \
        rmse < config['loglog_rmse_threshold']:

        if slope > config['loglog_tail_heavy_threshold']:
            warnings.warn("""
            Heavy-tail {0} distributions are usually hard to learn (slope={1})!
            Consider rolling up {0} or dropping its rare values.
            """.format(name, slope))

        elif slope < config['loglog_head_heavy_threshold']:
            warnings.warn("""
            Head-heavy {0} distributions are usually uninteresting or spammy (slope={1})!
            Consider using finer-grade {0} or thresholding its dominate values.
            """.format(name, slope))

    return (slope, intercept, rmse)


def describe_dataframe(df, name=''):
    print("\n=== Describe {} ===\n".format(name))
    with pd.option_context("display.max_rows", 100):
        print(df.describe(include='all'))

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


def compute_bootstrap_loss(df, freq, method):
    tic = time.time()

    df = df.copy()
    df['_bs'] = np.random.rand(len(df))<0.5

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
        c = 1
        X = Y*0
        X.eliminate_zeros()
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


def _fit_transform(method_at_k, q, p):
    topk = int(method_at_k.split('@')[1])
    indices = np.argsort(
        -q.toarray() + np.random.rand(*q.shape)*1e-10,
        axis=1)[:, :topk]
    p_topk = np.take_along_axis(p.toarray(), indices, axis=1)
    return p_topk


def compute_distribution_shift(index, df_wgt, Y, X, method, hist_len, freq=None, tic=0):
    """ Y:target (unobserved), X:data (observed) """

    N = Y.shape[1]
    p = _normalize_distribution(Y)
    q = _normalize_distribution(X)

    if method.lower() in ['kl', 'kl-divergence']:
        eps_ratio = (1-config['eps_greedy']) / (config['eps_greedy'] / N)
        log_p = (p * eps_ratio).log1p()
        log_q = (q * eps_ratio).log1p()
        temporal_loss = (p .multiply (log_p - log_q)).sum(axis=1)
        loss_fmt = '{:.2f}'

    elif method.lower() in ['ce', 'cross-entropy']:
        eps_ratio = (1-config['eps_greedy']) / (config['eps_greedy'] / N)
        log_q = (q * eps_ratio).log1p()
        temporal_loss = -((p .multiply (log_q)).sum(axis=1) + \
                        np.log(config['eps_greedy'] / N))
        loss_fmt = '{:.2f}'

    elif method.lower() in ['oov', 'out-sample items']:
        temporal_loss = 1.0 - (p .multiply (q>0)).sum(axis=1)
        loss_fmt = '{:.1%}'

    elif method.lower() in ['tv', 'total variation']:
        temporal_loss = (p-q).multiply(p>q).sum(axis=1)
        loss_fmt = '{:.1%}'

    elif method.lower().startswith('hit@'):
        p_topk = _fit_transform(method, q, p)
        temporal_loss = -p_topk.sum(axis=1)
        loss_fmt = '{:.1%}'

    elif method.lower().startswith('mrr@'):
        topk = int(method.split('@')[1])
        p_topk = _fit_transform(method, q, p)
        temporal_loss = -(p_topk / (1+np.arange(topk))[None,:]).sum(axis=1)
        loss_fmt = '{:.1%}'

    else:
        raise NotImplementedError

    temporal_loss = pd.Series(np.ravel(temporal_loss), index=index)

    avg_loss = np.average(temporal_loss.values, weights=df_wgt.values)

    print('temporal {}, freq={}, hist_len={}, avg_loss={}, time={:.1f}s'.format(
        method, freq, hist_len, loss_fmt.format(avg_loss), time.time() - tic,
    ))
    return temporal_loss, df_wgt, avg_loss, loss_fmt


def diagnose_interactions(df):
    print("\n=== Interactions table, original shape={} ===\n"
          .format(df.shape))
    df = df.copy()
    df['ITEM_ID'] = df['ITEM_ID'].astype(str)
    df['USER_ID'] = df['USER_ID'].astype(str)
    df.index = df["TIMESTAMP"].values.astype("datetime64[s]")

    if config['na_rate_threshold'] < 1:
        na_rate = df[config['interactions_required_fields']].isnull().any(axis=1).mean()
        print("missing rate in fields", config['interactions_required_fields'], na_rate)
        if na_rate > config['na_rate_threshold']:
            warnings.warn("High data missing rate for required fields ({:.1%})!".format(na_rate))
        df = df.dropna(subset=config['interactions_required_fields'])
        print("dropna shape", df.shape)


    if config['dup_rate_threshold'] < 1:
        dup_rate = (df.groupby(config['interactions_required_fields']).size() - 1.0).sum() / df.shape[0]
        print("duplication rate", dup_rate)
        if dup_rate > config['dup_rate_threshold']:
            warnings.warn("""
            High duplication rate ({:.1%})!
            Only one event can be taken at the same (user,item,timestamp) index.
            """.format(dup_rate))

        df = df.drop_duplicates(subset=config['interactions_required_fields'])
        print("drop_duplicates shape", df.shape)


    if config['repeat_rate_threshold'] < 1:
        repeat_rate = (df.groupby(["USER_ID", "ITEM_ID"]).size() - 1.0).sum() / df.shape[0]
        print("user item repeat rate", repeat_rate)
        if repeat_rate > config['repeat_rate_threshold']:
            warnings.warn("""
            High rate of repeated consumptions ({:.1%})!
            We would not do anything, but it may beneficial to
            (1) consider keeping only the last interaction between the same user-item pair,
            (2) consider if the ITEM_IDs have collisions, and/or
            (3) use high-order hierarchical models.
            """.format(repeat_rate))

    if config['describe_dataframe']:
        summary = describe_dataframe(df, 'interactions table')


    if config['show_activity_patterns']:
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
    print("Sorting...")
    df.sort_index(inplace=True, kind='mergesort')
    if config['temporal_shift_dedup']:
        print("Removing repeated user-items...")
        df_dedup = df.drop_duplicates(['USER_ID','ITEM_ID'], keep='last')
    else:
        df_dedup = df.copy()

    print("\n=== Temporal shift - retrain frequency ===\n")

    for method in config['temporal_loss_methods']:
        bootstrap_avg = []
        past_fut_avg  = []
        for freq in config['retrain_frequencies']:
            _, _, _bs_avg, loss_fmt = compute_bootstrap_loss(df_dedup, freq, method)
            _, _, _ts_avg, loss_fmt = compute_temporal_loss(df_dedup, freq, method, 1)
            bootstrap_avg.append(_bs_avg)
            past_fut_avg.append(_ts_avg)
        pl.plot(config['retrain_frequencies'], bootstrap_avg, '.--', label='same-period bootstrap')
        pl.plot(config['retrain_frequencies'], past_fut_avg, '.-', label='lagged popularity')
        pl.legend()
        pl.xlabel('retrain frequency')
        pl.title(method + ' loss at different frequencies')
        pl.grid()
        pl.gca().yaxis.set_major_formatter(pl.FuncFormatter(lambda y, _: loss_fmt.format(y)))
        pl.show()


    print("\n=== Temporal shift - history cutoffs ===\n")

    freq = config['retrain_frequencies'][-1]
    for i,(p,b) in list(enumerate(zip(past_fut_avg, bootstrap_avg)))[::-1]:
        if p<b:
            freq = config['retrain_frequencies'][i]

    for method in config['temporal_loss_methods']:
        bootstrap_loss, _, avg_loss, loss_fmt = compute_bootstrap_loss(df_dedup, freq, method)
        pl.plot(bootstrap_loss.iloc[-config['temporal_plot_limit']:], '.--',
                    label = 'boostrap baseline={}'.format(loss_fmt.format(avg_loss)))

        for hist_len in config['rolling_history_lags']:
            temporal_loss, df_wgt, avg_loss, loss_fmt = compute_temporal_loss(df_dedup, freq, method, hist_len)

            pl.plot(temporal_loss.iloc[-config['temporal_plot_limit']:], '.-',
                    label = 'hist={} * {}, avg={}'.format(hist_len, freq, loss_fmt.format(avg_loss)))

        pl.gca().yaxis.set_major_formatter(pl.FuncFormatter(lambda y, _: loss_fmt.format(y)))

        pl.title('{} {} from rolling history (lower is better)'.format(freq, method))
        pl.grid()
        pl.gcf().autofmt_xdate()
        pl.legend(loc='upper left')
        pl.twinx()
        pl.plot(df_wgt.iloc[-config['temporal_plot_limit']:], color='grey', lw=3, ls='--', alpha=0.5)
        pl.legend(['activity density'], loc='upper right')
        pl.show()

    if config['describe_sessions']:
        print("\n=== describe sessions ===")

        user_time_delta = df.groupby('USER_ID')["TIMESTAMP"].transform(pd.Series.diff).dropna()
        user_time_delta.sort_values(ascending=False, inplace=True)
        print(user_time_delta.describe())
        plot_loglog(user_time_delta, 'session time delta', show=False)
        for k,v in config['timedelta_references'].items():
            if pl.ylim()[0] < v < pl.ylim()[1]:
                pl.plot(pl.xlim(), [v,v], '--')
                pl.text(pl.xlim()[0], v, k)
        pl.show()


        user_time_span = df.groupby('USER_ID')["TIMESTAMP"].apply(lambda x:max(x)-min(x))
        user_time_span.sort_values(ascending=False, inplace=True)
        print("=== user time span describe ===")
        print(user_time_span.describe())
        plot_loglog(user_time_span, 'user time span', show=False)
        for k,v in config['timedelta_references'].items():
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

    if config['na_rate_threshold'] < 1:
        missing_rate = 1 - df.USER_ID.astype(str).isin(set(users.index.values)).mean()
        print("Missing rate of all user meta-data", missing_rate)
        if missing_rate > config['na_rate_threshold']:
            warnings.warn("High missing rate of all user meta-data ({:%})!"
                          .format(missing_rate))

    if config['coldstart_rate_threshold'] < 1:
        coldstart_rate = 1 - users.index.isin(set(df.USER_ID.astype(str).values)).mean()
        print("User coldstart rate", coldstart_rate)
        if coldstart_rate > config['coldstart_rate_threshold']:
            warnings.warn("High user coldstart rate ({:%})!"
                          .format(coldstart_rate))

    describe_dataframe(users)


def diagnose_items(df, items):
    print("\n=== Items table, original shape={} ===\n"
          .format(items.shape))
    items = items.copy()
    items['ITEM_ID'] = items['ITEM_ID'].astype(str)
    items = items.set_index('ITEM_ID')

    if config['na_rate_threshold'] < 1:
        missing_rate = 1 - df.ITEM_ID.astype(str).isin(set(items.index.values)).mean()
        print("Missing rate of all item meta-data", missing_rate)
        if missing_rate > config['na_rate_threshold']:
            warnings.warn("High missing rate of all item meta-data ({:%})!"
                          .format(missing_rate))

    if config['coldstart_rate_threshold'] < 1:
        coldstart_rate = 1 - items.index.isin(set(df.ITEM_ID.astype(str).values)).mean()
        print("Item coldstart rate", coldstart_rate)
        if coldstart_rate > config['coldstart_rate_threshold']:
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

if args.datasets is not None and len(args.datasets):
    diagnose(*[pd.read_csv(d) for d in args.datasets])
