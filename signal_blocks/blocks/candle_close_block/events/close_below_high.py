def main(df, action):
    df["order"] = None
    df.loc[df.close.astype(float) < df.high.astype(float), "order"] = action
    return df