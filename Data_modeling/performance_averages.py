import pandas as pd
import numpy as np
def performance_averages(goalie_df, defender_df, midfielder_df, forward_df, match_df):
    # Define a decay-weighted rolling average function
    def decay_weighted_avg(series, decay_factor):
        n = len(series)
        weights = np.array([decay_factor**i for i in range(n)][::-1])  # Exponential decay
        weights /= weights.sum()  # Normalize weights
        return (series * weights).sum()

    # Apply decay-weighted averages for each column
    decay_factor = 0.7  # Tune this value for your decay
    goalie_df['penalties_saved_last_5'] = (goalie_df.groupby('player_id')['penalties_saved'].apply(lambda x: x.rolling(window=5, min_periods=1).apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))).reset_index(level=0, drop=True)

    goalie_df['saves_last_5'] = (goalie_df.groupby('player_id')['saves'].apply(lambda x: x.rolling(window=5, min_periods=1).apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))).reset_index(level=0, drop=True)

    goalie_df['clean_sheets_last_5'] = (goalie_df.groupby('player_id')['clean_sheets'].apply(lambda x: x.rolling(window=5, min_periods=1).apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))).reset_index(level=0, drop=True)

    goalie_df['bps_last_5'] = (goalie_df.groupby('player_id')['bps'].apply(lambda x: x.rolling(window=5, min_periods=1).apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))).reset_index(level=0, drop=True)

    goalie_df['minutes_last_5'] = (goalie_df.groupby('player_id')['minutes'].apply(lambda x: x.rolling(window=5, min_periods=1).apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))).reset_index(level=0, drop=True)


    # Defender rolling averages
    defender_df['saves_last_5'] = (
        defender_df.groupby('player_id')['saves']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    defender_df['clean_sheets_last_5'] = (
        defender_df.groupby('player_id')['clean_sheets']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    defender_df['own_goals_last_5'] = (
        defender_df.groupby('player_id')['own_goals']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    defender_df['bps_last_5'] = (
        defender_df.groupby('player_id')['bps']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    defender_df['minutes_last_5'] = (
        defender_df.groupby('player_id')['minutes']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    # Midfielder rolling averages
    midfielder_df['goals_scored_last_5'] = (
        midfielder_df.groupby('player_id')['goals_scored']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    midfielder_df['assists_last_5'] = (
        midfielder_df.groupby('player_id')['assists']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    midfielder_df['threat_last_5'] = (
        midfielder_df.groupby('player_id')['threat']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    midfielder_df['bps_last_5'] = (
        midfielder_df.groupby('player_id')['bps']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    midfielder_df['minutes_last_5'] = (
        midfielder_df.groupby('player_id')['minutes']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    # Forward rolling averages
    forward_df['goals_scored_last_5'] = (
        forward_df.groupby('player_id')['goals_scored']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    forward_df['assists_last_5'] = (
        forward_df.groupby('player_id')['assists']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    forward_df['threat_last_5'] = (
        forward_df.groupby('player_id')['threat']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    forward_df['bps_last_5'] = (
        forward_df.groupby('player_id')['bps']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    forward_df['minutes_last_5'] = (
        forward_df.groupby('player_id')['minutes']
        .apply(lambda x: x.rolling(window=5, min_periods=1)
        .apply(lambda y: decay_weighted_avg(y, decay_factor=decay_factor), raw=False))
    ).reset_index(level=0, drop=True)

    goalie_df = goalie_df[goalie_df['minutes_last_5'] > 0]
    defender_df = defender_df[defender_df['minutes_last_5'] > 0]
    midfielder_df = midfielder_df[midfielder_df['minutes_last_5'] > 0]
    forward_df = forward_df[forward_df['minutes_last_5'] > 0]

    goalie_df = goalie_df[['player_id', 'kickoff_time', 'penalties_saved_last_5', 'saves_last_5', 'clean_sheets_last_5', 'minutes_last_5','bps_last_5', 'total_points', 'form']]
    defender_df = defender_df[['player_id', 'kickoff_time', 'saves_last_5', 'clean_sheets_last_5', 'own_goals_last_5', 'bps_last_5', 'minutes_last_5', 'total_points', 'form']]
    midfielder_df = midfielder_df[['player_id', 'kickoff_time', 'goals_scored_last_5', 'assists_last_5', 'minutes_last_5', 'threat_last_5', 'bps_last_5', 'total_points', 'form']]
    forward_df = forward_df[['player_id', 'kickoff_time', 'goals_scored_last_5', 'assists_last_5', 'minutes_last_5', 'threat_last_5', 'bps_last_5', 'total_points', 'form']]
    # 1. Concatenate position DataFrames:
    all_positions_df = pd.concat([goalie_df, defender_df, midfielder_df, forward_df])

    # 2. Merge rolling averages into match_df:
    match_df = pd.merge(
        match_df,
        all_positions_df[['player_id', 'kickoff_time', 'penalties_saved_last_5', 'saves_last_5', 'clean_sheets_last_5', 'goals_scored_last_5', 'assists_last_5', 'minutes_last_5', 'threat_last_5', 'bps_last_5', 'own_goals_last_5']],  # Select relevant columns
        on=['player_id', 'kickoff_time'],
        how='left'  # Use a left merge to keep all rows in match_df
    )
    # Ensure numeric data types for relevant columns in match_df
    numeric_columns = ['goals_scored', 'assists', 'minutes', 'yellow_cards', 'threat', 'penalties_saved', 'saves', 'clean_sheets', 'own_goals', 'bps', 'form']
    match_df[numeric_columns] = match_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Drop rows where all numeric columns are NaN to avoid empty rows in calculations
    match_df = match_df.dropna(subset=numeric_columns, how='all')

    return match_df