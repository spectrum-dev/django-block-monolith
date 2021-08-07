def main(df, action, crossover_value):
    df = df.dropna()
    df["order"] = None

    i = 1
    while i < df.shape[0]:
        prev_value = df["data"][i - 1]
        current_value = df["data"][i]

        # If current indicator value is below crossover point and is not a consecutive crossover, then place action
        if current_value > crossover_value and prev_value <= crossover_value:
            df["order"][i] = action
        i += 1

    return df
