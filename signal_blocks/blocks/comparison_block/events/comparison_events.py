def less_than(df, action):
    df["order"] = None
    df.loc[
        df.comparison_field_1.astype(float) < df.comparison_field_2.astype(float),
        "order",
    ] = action
    return df


def less_than_equal(df, action):
    df["order"] = None
    df.loc[
        df.comparison_field_1.astype(float) <= df.comparison_field_2.astype(float),
        "order",
    ] = action
    return df


def more_than(df, action):
    df["order"] = None
    df.loc[
        df.comparison_field_1.astype(float) > df.comparison_field_2.astype(float),
        "order",
    ] = action
    return df


def more_than_equal(df, action):
    df["order"] = None
    df.loc[
        df.comparison_field_1.astype(float) >= df.comparison_field_2.astype(float),
        "order",
    ] = action
    return df
