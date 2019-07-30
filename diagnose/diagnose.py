import pandas as pd
import pylab as pl
import numpy as np


def plot_loglog(val, name=''):
    x = 1+np.arange(len(val))
    slope, intercept = np.polyfit(np.log10(x)[val>0], np.log10(val[val>0]), deg=1)
    fitted = 10**(intercept + slope*np.log10(x))
    pl.loglog(x, val)
    pl.loglog(x, fitted, ':')
    pl.grid()
    pl.title(name + ' loglog, %.2f * x^(%.2f)'%(10**intercept, slope))
    pl.show()


def describe_categorical(sr, name=''):
    parts = sr.apply(lambda x: str(x).split('|'))
    print(name, ' multi-category stats:')
    print(parts.apply(len).describe())
    print(name, ' top categories:')
    cats = pd.Series(np.hstack(parts.values))
    cats_freq = cats.groupby(cats).size().sort_values(ascending=False)
    print(cats_freq.head(10))
    plot_loglog(cats_freq, name)


def describe_dataframe(df, name=''):
    print("DESCRIBE ", name)
    print(df.describe(include='all'))
    for cn, dtype in df.dtypes.iteritems():
        if dtype == object:
            describe_categorical(df[cn], cn)        


def diagnose_interactions(df):
    print("original interactions shape", df.shape)

    df = df.dropna()
    print("dropna shape", df.shape)

    df = df.drop_duplicates(subset=["USER_ID","ITEM_ID","TIMESTAMP"])
    print("drop_duplicates shape", df.shape)

    print("optional without repeated purchases shape",
          df.drop_duplicates(subset=["USER_ID","ITEM_ID"]).shape)

    print("=== unique USER_ID describe ===")
    user_freq = df.groupby("USER_ID").size().sort_values(ascending=False)
    print(user_freq.describe())
    plot_loglog(user_freq, 'user freq')

    print("=== unique ITEM_ID describe ===")
    item_freq = df.groupby("ITEM_ID").size().sort_values(ascending=False)
    print(item_freq.describe())
    plot_loglog(item_freq, 'item freq')

    # sequence analysis
    df.index = df["TIMESTAMP"].values.astype("datetime64[s]")
    df.sort_index(inplace=True)

    print("=== hourly activity pattern ===")
    print(df.groupby(df.index.hour).size())

    print("=== day of week activity pattern ===")
    print(df.groupby(df.index.dayofweek).size())
    
    plot_patterns = {
        "date": df.index.date,
        "hour": df.index.hour,
        "dayofweek": df.index.dayofweek}

    for k,v in plot_patterns.items():
        pl.plot(df.groupby(v).size())
        pl.gcf().autofmt_xdate()
        pl.title("activity pattern by %s" %k)
        pl.grid()
        pl.show()

    print("=== session time delta describe ===")
    user_time_delta = df.groupby('USER_ID')["TIMESTAMP"].transform(pd.Series.diff).dropna()
    user_time_delta.sort_values(ascending=False, inplace=True)
    print(user_time_delta.describe())
    plot_loglog(user_time_delta, 'session time delta')

    user_time_span = df.groupby('USER_ID')["TIMESTAMP"].apply(np.ptp)
    user_time_span.sort_values(ascending=False, inplace=True)
    print("=== user time span describe ===")
    print(user_time_span.describe())
    plot_loglog(user_time_span, 'user time span')

    # temporal shift analysis
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
    print("=== user meta-data missing rate ===")
    print(users.isnull().mean())

    print("rate of interactions without user meta-data",
          (~df.USER_ID.isin(set(users.USER_ID.values))).mean())

    print("rate of new users not referenced in interactions table",
          (~users.USER_ID.isin(set(df.USER_ID.values))).mean())


def diagnose_items(df, items):
    print("=== item meta-data missing rate ===")
    print(items.isnull().mean())

    print("rate of interactions without item meta-data",
          (~df.ITEM_ID.isin(set(items.ITEM_ID.values))).mean())

    print("rate of new items not referenced in interactions table",
          (~items.ITEM_ID.isin(set(df.ITEM_ID.values))).mean())

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
    describe_dataframe(df)
    diagnose_interactions(df)

    if users is not None:
        print("########################################")
        print("# DIAGNOSING USERS TABLE, SAMPLE:")
        print("########################################")
        print(users.sample(min(len(users), 10)))
        describe_dataframe(users)
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
        describe_dataframe(items)
        diagnose_items(df, items)
    else:
        print("########################################")
        print("# ITEMS TABLE NOT FOUND")
        print("########################################")
