import pandas as pd
import pylab as pl
import numpy as np
import warnings


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
ROLLING_HISTORY_LEN = [1, 7, 31, 365]


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


def compute_daily_divergence(daily_count, alpha, hist_len):
    N = daily_count.shape[1]
    X = daily_count.rolling(hist_len, min_periods=1).sum().iloc[:-1]
    Y = daily_count.iloc[1:]
    index = Y.index

    # data (observed)
    gz = (X > 0).values
    p  = X.apply(lambda x:x/(sum(x) + 1e-20), axis=1).values * (1-EPS_GREEDY) + (EPS_GREEDY / N)

    # target (unobserved)
    q  = Y.apply(lambda x:x/(sum(x) + 1e-20), axis=1).values * (1-EPS_GREEDY) + (EPS_GREEDY / N)

    if alpha==1:
        daily_divergence = (p * (np.log(p) - np.log(q))).sum(axis=1)
    elif alpha==0:
        Q = np.sum( q * gz, axis=1)
        daily_divergence = np.log(np.clip(Q, 1e-20, np.inf)) / (alpha-1)
    else:
        daily_divergence = np.log( (p ** alpha / q ** (alpha-1)).sum(axis=1) ) / (alpha-1)


    daily_divergence = pd.Series(daily_divergence, index=index)
    return daily_divergence


def diagnose_interactions(df):
    print("\n=== Interactions table, original shape={} ===\n"
          .format(df.shape))
    df = df.copy()
    df['ITEM_ID'] = df['ITEM_ID'].astype(str)
    df['USER_ID'] = df['USER_ID'].astype(str)


    na_rate = df[INTERACTIONS_REQUIRED_FIELDS].isnull().any(axis=1).mean()
    print("missing rate in fields", INTERACTIONS_REQUIRED_FIELDS, na_rate)
    if na_rate > NA_RATE_THRESHOLD:
        warnings.warn("High data missing rate for required fields!")
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


    print("\n=== Sequence analysis ===\n")
    df.index = df["TIMESTAMP"].values.astype("datetime64[s]")
    df.sort_index(inplace=True)

    print("\n=== Hourly activity pattern ===")
    print(df.groupby(df.index.hour).size())

    print("\n=== Day of week activity pattern ===")
    print(df.groupby(df.index.dayofweek).size())

    plot_patterns = {
        "date": df.index.date,
        "hour": df.index.hour,
        "dayofweek": df.index.dayofweek}

    for k,v in plot_patterns.items():
        pl.plot(df.groupby(v).size())
        pl.gcf().autofmt_xdate()
        pl.title("Activity pattern by %s" %k)
        pl.grid()
        pl.show()

    print("\n=== session time delta describe ===")
    user_time_delta = df.groupby('USER_ID')["TIMESTAMP"].transform(pd.Series.diff).dropna()
    user_time_delta.sort_values(ascending=False, inplace=True)
    print(user_time_delta.describe())
    plot_loglog(user_time_delta, 'session time delta', show=False)
    for k,v in TIMEDELTA_REFERENCES:
        if pl.ylim()[0] < v < pl.ylim()[1]:
            pl.plot(pl.xlim(), [v,v], '--')
            pl.text(pl.xlim()[0], v, k)
    pl.show()


    user_time_span = df.groupby('USER_ID')["TIMESTAMP"].apply(np.ptp)
    user_time_span.sort_values(ascending=False, inplace=True)
    print("=== user time span describe ===")
    print(user_time_span.describe())
    plot_loglog(user_time_span, 'user time span', show=False)
    for k,v in TIMEDELTA_REFERENCES:
        if pl.ylim()[0] < v < pl.ylim()[1]:
            pl.plot(pl.xlim(), [v,v], '--')
            pl.text(pl.xlim()[0], v, k)
    pl.show()


    print("\n=== Temporal shift analysis ===\n")
    daily_count = df.groupby([df.index.date, 'ITEM_ID']).size().unstack().fillna(0)
    daily_count.index = daily_count.index.astype('datetime64[ns]')
    date_range  = pd.date_range(daily_count.index.min(), daily_count.index.max())
    daily_count = daily_count.reindex(date_range, fill_value=0)

    for hist_len in ROLLING_HISTORY_LEN:
        daily_renyi = compute_daily_divergence(daily_count, 0, hist_len)
        pl.plot(1-np.exp(-daily_renyi), '.-',
                label='history={} days'.format(hist_len))
    pl.title('Daily percent new items with rolling history')
    pl.gcf().autofmt_xdate()
    pl.legend()
    pl.show()


    for hist_len in ROLLING_HISTORY_LEN:
        daily_renyi = compute_daily_divergence(daily_count, 1, hist_len)
        pl.plot(daily_renyi, '.-',
                label='history={} days'.format(hist_len))
    pl.title('Daily KL divergence with rolling history')
    pl.gcf().autofmt_xdate()
    pl.legend()
    pl.show()


    date_and_item_size = df.groupby([df.index.date, 'ITEM_ID']).size().to_frame(
        'size').reset_index('ITEM_ID').sort_values('size', ascending=False)

    print("=== number of days when an item stays as daily top-1 ===")
    daily_top_1s = date_and_item_size.groupby(level=0).head(
        1).groupby('ITEM_ID').size().sort_values(ascending=False)
    print(daily_top_1s.head(10))

    print("=== number of days when an item stays in daily top-5 ===")
    daily_top_5s = date_and_item_size.groupby(level=0).head(
        5).groupby('ITEM_ID').size().sort_values(ascending=False)
    print(daily_top_5s.head(10))


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
