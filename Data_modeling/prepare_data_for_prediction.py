import pandas as pd
from Data_modeling.extract_api import *
def prepare_data_for_prediction(future_fixtures_df, match_df):
    future_fixtures_df = future_fixtures_df.rename(columns={'difficulty': 'match_difficulty'})
    goalie_data = []
    defender_data = []
    midfielder_data = []
    forward_data = []
    seen = {}
    
    for _, fixture in future_fixtures_df.iterrows():
        if fixture['player_id'] not in seen:
            seen[fixture['player_id']] = True
            player_id = fixture['player_id']
            position = fixture['position']
            kickoff_time = pd.to_datetime(fixture['kickoff_time'], utc=True)
            match_difficulty = fixture['match_difficulty']  # Use specific match difficulty

            # Sort by kickoff_time to get last 3 matches before this fixture
            player_matches = match_df[match_df['player_id'] == player_id].sort_values(by=['kickoff_time'], ascending=False)
            player_matches['kickoff_time'] = pd.to_datetime(player_matches['kickoff_time'], utc=True)

            # Select last 3 matches and their rolling average features
            last_match = player_matches[player_matches['kickoff_time'] < kickoff_time][[
                'player_id', 'position',
                'penalties_saved_last_5', 'saves_last_5', 'clean_sheets_last_5',
                'goals_scored_last_5', 'assists_last_5', 'minutes_last_5', 'bps_last_5', 'own_goals_last_5', 'form', 'points_per_game','ict_index_last_5'
            ]].head(1)

            if not last_match.empty:
                # Add difficulty as a feature for the specific match
                if position == 'goalkeeper':
                    features = last_match[['penalties_saved_last_5', 'saves_last_5', 'clean_sheets_last_5','minutes_last_5', 'bps_last_5', 'form', 'points_per_game','ict_index_last_5']].iloc[-1].to_dict()
                    features['player_id'] = player_id
                    features['match_difficulty'] = match_difficulty  # Changed key to 'match_difficulty'
                    features = {k.replace("_last_5", ""): v for k, v in features.items()}
                    goalie_data.append(features)
                elif position == 'defender':
                    features = last_match[['saves_last_5', 'clean_sheets_last_5', 'own_goals_last_5', 'bps_last_5', 'minutes_last_5', 'form', 'points_per_game','ict_index_last_5']].iloc[-1].to_dict()
                    features['player_id'] = player_id
                    features['match_difficulty'] = match_difficulty  # Changed key to 'match_difficulty'
                    features = {k.replace("_last_5", ""): v for k, v in features.items()}
                    defender_data.append(features)
                elif position == 'midfielder':
                    features = last_match[['goals_scored_last_5', 'assists_last_5', 'bps_last_5', 'minutes_last_5', 'form', 'points_per_game','ict_index_last_5']].iloc[-1].to_dict()
                    features['player_id'] = player_id
                    features['match_difficulty'] = match_difficulty  # Changed key to 'match_difficulty'
                    features = {k.replace("_last_5", ""): v for k, v in features.items()}
                    midfielder_data.append(features)
                elif position == 'forward':
                    features = last_match[['goals_scored_last_5', 'assists_last_5', 'bps_last_5', 'minutes_last_5', 'form', 'points_per_game','ict_index_last_5']].iloc[-1].to_dict()
                    features['player_id'] = player_id
                    features['match_difficulty'] = match_difficulty  # Changed key to 'match_difficulty'
                    features = {k.replace("_last_5", ""): v for k, v in features.items()}
                    forward_data.append(features)

    # Convert lists of dictionaries to DataFrames for each position
    goalie_data = pd.DataFrame(goalie_data)
    defender_data = pd.DataFrame(defender_data)
    midfielder_data = pd.DataFrame(midfielder_data)
    forward_data = pd.DataFrame(forward_data)
    return goalie_data, defender_data, midfielder_data, forward_data
