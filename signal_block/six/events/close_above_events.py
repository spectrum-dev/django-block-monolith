def close_above_low(df, action):
    df["order"] = None
    df.loc[df.close.astype(float) > df.low.astype(float), "order"] = action
    return df


def close_above_open(df, action):
    df["order"] = None
    df.loc[df.close.astype(float) > df.open.astype(float), "order"] = action
    return df


def close_below_high(df, action):
    df["order"] = None
    df.loc[df.close.astype(float) < df.high.astype(float), "order"] = action
    return df


def close_below_open(df, action):
    df["order"] = None
    df.loc[df.close.astype(float) < df.open.astype(float), "order"] = action
    return df


def close_eq_high(df, action):
    df["order"] = None
    df.loc[df.close.astype(float) >= df.high.astype(float), "order"] = action
    return df


def close_eq_low(df, action):
    df["order"] = None
    df.loc[df.close.astype(float) <= df.low.astype(float), "order"] = action
    return df
