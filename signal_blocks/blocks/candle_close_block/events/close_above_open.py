def main(df, action):
    df["order"] = None
    df.loc[df.close.astype(float) > df.open.astype(float), "order"] = action
    return df
