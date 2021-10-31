def main(df, action, crossover_value):
    df = df.dropna()
    df["order"] = None
    # If current indicator value is above crossover point and is not a consecutive crossover, then place action
    df.loc[
        (df.data > crossover_value) & (df.data.shift(1) <= crossover_value), "order"
    ] = action

    return df
