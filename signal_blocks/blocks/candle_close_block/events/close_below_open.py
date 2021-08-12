def main(df, action):
    df["order"] = None
    df.loc[df.close < df.open, "order"] = action
    return df