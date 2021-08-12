def main(df, action):
    df["order"] = None
    df.loc[df.close.astype(float) > df.low.astype(float), "order"] = action
    return df
