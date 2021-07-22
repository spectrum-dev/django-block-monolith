def main(df, action, consecutive_down, consecutive_up):
    df['percent_change'] = df.pct_change(periods=1)
    df = df.dropna()
    df['order'] = None

    i = 0
    while (i < (df.shape[0] - (consecutive_down + consecutive_up))):
        downward_df = df.iloc[i : i + consecutive_down]
        upward_df = df.iloc[i + consecutive_down : i + consecutive_down + consecutive_up]

        if ((downward_df['percent_change'] < 0).all() and (upward_df['percent_change'] > 0).all()):
            df['order'][i + consecutive_down + consecutive_up] = action
        
        i += 1

    return df