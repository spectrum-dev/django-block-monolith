def main(df, action):
    df["order"] = None
    df.loc[df.close > df.low, "order"] = action
    return df