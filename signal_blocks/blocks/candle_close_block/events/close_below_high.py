def main(df, action):
    df["order"] = None
    df.loc[df.close <= df.high, "order"] = action
    return df