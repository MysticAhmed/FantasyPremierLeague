import pandas as pd
import numpy as np
def performance_averages(goalie_df, defender_df, midfielder_df, forward_df, match_df):
    #goalie rolling averages for predictions
    goalie_df.loc[:,'penalties_saved_last_5'] = goalie_df.groupby('player_id')['penalties_saved'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    goalie_df.loc[:,'saves_last_5'] = goalie_df.groupby('player_id')['saves'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    goalie_df.loc[:,'clean_sheets_last_5'] = goalie_df.groupby('player_id')['clean_sheets'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    goalie_df.loc[:,'bps_last_5'] = goalie_df.groupby('player_id')['bps'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    goalie_df.loc[:,'minutes_last_5'] = goalie_df.groupby('player_id')['minutes'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    goalie_df.loc[:,'ict_index_last_5'] = goalie_df.groupby('player_id')['ict_index'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)

    #defender rolling averages for predictions
    defender_df.loc[:,'saves_last_5'] = defender_df.groupby('player_id')['saves'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    defender_df.loc[:,'clean_sheets_last_5'] = defender_df.groupby('player_id')['clean_sheets'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    defender_df.loc[:,'own_goals_last_5'] = defender_df.groupby('player_id')['own_goals'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    defender_df.loc[:,'bps_last_5'] = defender_df.groupby('player_id')['bps'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    defender_df.loc[:,'minutes_last_5'] = defender_df.groupby('player_id')['minutes'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    defender_df.loc[:,'ict_index_last_5'] = defender_df.groupby('player_id')['ict_index'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    #midfielder rolling averages for predictions
    midfielder_df.loc[:,'goals_scored_last_5'] = midfielder_df.groupby('player_id')['goals_scored'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    midfielder_df.loc[:,'assists_last_5'] = midfielder_df.groupby('player_id')['assists'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    midfielder_df.loc[:,'bps_last_5'] = midfielder_df.groupby('player_id')['bps'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    midfielder_df.loc[:,'minutes_last_5'] = midfielder_df.groupby('player_id')['minutes'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    midfielder_df.loc[:,'ict_index_last_5'] = midfielder_df.groupby('player_id')['ict_index'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)

    #defender rolling averages for predictions
    forward_df.loc[:,'goals_scored_last_5'] = forward_df.groupby('player_id')['goals_scored'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    forward_df.loc[:,'assists_last_5'] = forward_df.groupby('player_id')['assists'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    forward_df.loc[:,'bps_last_5'] = forward_df.groupby('player_id')['bps'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    forward_df.loc[:,'minutes_last_5'] = forward_df.groupby('player_id')['minutes'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)
    forward_df.loc[:,'ict_index_last_5'] = forward_df.groupby('player_id')['ict_index'].rolling(window=6, min_periods=1).mean().reset_index(0, drop=True)

    goalie_df = goalie_df[goalie_df['minutes_last_5'] > 0]
    defender_df = defender_df[defender_df['minutes_last_5'] > 0]
    midfielder_df = midfielder_df[midfielder_df['minutes_last_5'] > 0]
    forward_df = forward_df[forward_df['minutes_last_5'] > 0]

    goalie_df = goalie_df[['player_id', 'kickoff_time', 'penalties_saved_last_5', 'saves_last_5', 'clean_sheets_last_5', 'minutes_last_5','bps_last_5', 'total_points', 'form', 'points_per_game','ict_index_last_5']]
    defender_df = defender_df[['player_id', 'kickoff_time', 'saves_last_5', 'clean_sheets_last_5', 'own_goals_last_5', 'bps_last_5', 'minutes_last_5', 'total_points', 'form', 'points_per_game','ict_index_last_5']]
    midfielder_df = midfielder_df[['player_id', 'kickoff_time', 'goals_scored_last_5', 'assists_last_5', 'minutes_last_5', 'bps_last_5', 'total_points', 'form', 'points_per_game','ict_index_last_5']]
    forward_df = forward_df[['player_id', 'kickoff_time', 'goals_scored_last_5', 'assists_last_5', 'minutes_last_5', 'bps_last_5', 'total_points', 'form', 'points_per_game','ict_index_last_5']]
    # 1. Concatenate position DataFrames:
    all_positions_df = pd.concat([goalie_df, defender_df, midfielder_df, forward_df])

    # 2. Merge rolling averages into match_df:
    match_df = pd.merge(
        match_df,
        all_positions_df[['player_id', 'kickoff_time', 'penalties_saved_last_5', 'saves_last_5', 'clean_sheets_last_5', 'goals_scored_last_5', 'assists_last_5', 'minutes_last_5', 'ict_index_last_5', 'bps_last_5', 'own_goals_last_5']],  # Select relevant columns
        on=['player_id', 'kickoff_time'],
        how='left'  # Use a left merge to keep all rows in match_df
    )

    return match_df