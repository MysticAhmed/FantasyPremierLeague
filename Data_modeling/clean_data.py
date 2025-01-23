import pandas as pd
import numpy as np
def clean_data(future_fixtures_df, match_df):
    match_df = match_df[match_df['minutes'] > 0]
    match_df = match_df.drop(columns=['id', 'home_team_reverse', 'away_team_reverse'])
    future_fixtures_df = future_fixtures_df.drop(columns=['id'])

    valid_player_ids = match_df['player_id'].unique()
    match_df['match_difficulty'] = match_df['match_difficulty'].fillna(3)
# Filter future_fixtures_df to only include rows with player IDs present in match_df
    future_fixtures_df = future_fixtures_df[future_fixtures_df['player_id'].isin(valid_player_ids)]
    
    goalie_df = match_df[(match_df['position'] == 'goalkeeper') &  (match_df['minutes'] > 0)].copy()
    defender_df = match_df[(match_df['position'] == 'defender') & (match_df['minutes'] > 0)].copy()
    midfielder_df = match_df[(match_df['position'] == 'midfielder') & (match_df['minutes'] > 0)].copy()
    forward_df = match_df[(match_df['position'] == 'forward') & (match_df['minutes'] > 0)].copy()

    numeric_columns = ['goals_scored', 'assists', 'minutes', 'yellow_cards', 'threat', 'penalties_saved', 'saves', 'clean_sheets', 'own_goals', 'bps', 'form']
    match_df[numeric_columns] = match_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Drop rows where all numeric columns are NaN to avoid empty rows in calculations
    match_df = match_df.dropna(subset=numeric_columns, how='all')
    # Convert 'kickoff_time' to datetime objects in match_df
    match_df['kickoff_time'] = pd.to_datetime(match_df['kickoff_time'], utc=True) 

    return future_fixtures_df, match_df