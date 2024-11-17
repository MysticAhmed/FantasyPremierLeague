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
            opponent_team = fixture['team_a'] if fixture['is_home'] else fixture['team_h']
            position = fixture['position']
            kickoff_time = pd.to_datetime(fixture['kickoff_time'], utc=True)
            match_difficulty = fixture['match_difficulty']

            # Check for last matchup stats
            last_matchup = get_last_matchup_stats(player_id, opponent_team, match_df)
            if last_matchup is not None:
                # Select features based on position
                if position == 'goalkeeper':
                    features = last_matchup[['penalties_saved', 'saves', 'clean_sheets', 'minutes', 'bps', 'form']].to_dict()
                elif position == 'defender':
                    features = last_matchup[['saves', 'clean_sheets', 'own_goals', 'bps', 'minutes', 'form']].to_dict()
                elif position == 'midfielder':
                    features = last_matchup[['goals_scored', 'assists', 'threat', 'bps', 'minutes', 'form']].to_dict()
                elif position == 'forward':
                    features = last_matchup[['goals_scored', 'assists', 'threat', 'bps', 'minutes', 'form']].to_dict()
            else:
                # Calculate rolling averages based on position
                player_matches = match_df[(match_df['player_id'] == player_id) & (match_df['kickoff_time'] < kickoff_time)]
                player_matches = player_matches.sort_values(by='kickoff_time', ascending=False).head(5)
                if position == 'goalkeeper':
                    features = {
                        'penalties_saved': player_matches['penalties_saved'].mean(),
                        'saves': player_matches['saves'].mean(),
                        'clean_sheets': player_matches['clean_sheets'].mean(),
                        'minutes': player_matches['minutes'].mean(),
                        'bps': player_matches['bps'].mean(),
                        'form': player_matches['form'].mean()
                    }
                elif position == 'defender':
                    features = {
                        'saves': player_matches['saves'].mean(),
                        'clean_sheets': player_matches['clean_sheets'].mean(),
                        'own_goals': player_matches['own_goals'].mean(),
                        'bps': player_matches['bps'].mean(),
                        'minutes': player_matches['minutes'].mean(),
                        'form': player_matches['form'].mean()
                    }
                elif position == 'midfielder':
                    features = {
                        'goals_scored': player_matches['goals_scored'].mean(),
                        'assists': player_matches['assists'].mean(),
                        'threat': player_matches['threat'].mean(),
                        'bps': player_matches['bps'].mean(),
                        'minutes': player_matches['minutes'].mean(),
                        'form': player_matches['form'].mean()
                    }
                elif position == 'forward':
                    features = {
                        'goals_scored': player_matches['goals_scored'].mean(),
                        'assists': player_matches['assists'].mean(),
                        'threat': player_matches['threat'].mean(),
                        'bps': player_matches['bps'].mean(),
                        'minutes': player_matches['minutes'].mean(),
                        'form': player_matches['form'].mean()
                    }

            features['player_id'] = player_id
            features['match_difficulty'] = match_difficulty

            # Add features to appropriate dataset
            if position == 'goalkeeper':
                goalie_data.append(features)
            elif position == 'defender':
                defender_data.append(features)
            elif position == 'midfielder':
                midfielder_data.append(features)
            elif position == 'forward':
                forward_data.append(features)

    # Convert lists of dictionaries to DataFrames for each position
    goalie_data = pd.DataFrame(goalie_data)
    defender_data = pd.DataFrame(defender_data)
    midfielder_data = pd.DataFrame(midfielder_data)
    forward_data = pd.DataFrame(forward_data)
    return goalie_data, defender_data, midfielder_data, forward_data
