def main(df, action, consecutive_up, consecutive_down):
    df['percent_change'] = df.pct_change(periods=1)
    df = df.dropna()
    df['order'] = None

    i = 0
    while (i < (df.shape[0] - (consecutive_up + consecutive_down))):
        upward_df = df.iloc[i : i + consecutive_up]
        downward_df = df.iloc[i + consecutive_up : i + consecutive_up + consecutive_down]

        if ((upward_df['percent_change'] > 0).all() and (downward_df['percent_change'] < 0).all()):
            df['order'][i + consecutive_up + consecutive_down] = action
        
        i += 1

    return df