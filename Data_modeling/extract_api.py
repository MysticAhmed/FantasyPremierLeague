import time
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Get All Player Data (Including Position) from the FPL API
def get_player_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    data = response.json()

    # Extract player data with element_type (position) and IDs
    players = pd.DataFrame(data['elements'])
    position_map = {1: 'goalkeeper', 2: 'defender', 3: 'midfielder', 4: 'forward'}
    players['position'] = players['element_type'].map(position_map)
    players['full_name'] = players['first_name'] + ' ' + players['second_name']
    player_ids = players[['id', 'first_name', 'second_name', 'full_name', 'position', 'team_code', 'form', 'points_per_game']]
    return player_ids, data['teams']

# Step 2: Get Team Data
def get_team_data(teams):
    teams_df = pd.DataFrame(teams)
    teams_data = teams_df[['id', 'code', 'name', 'short_name', 'strength_overall_home', 'strength_overall_away']]
    return teams_data

# Step 3: Fetch player data from element-summary endpoint
def get_player_data_from_summary(player_id):
    player_ids, team = get_player_data()
    player_url = f"https://fantasy.premierleague.com/api/element-summary/{player_id}/"
    response = requests.get(player_url)
    player_data = response.json()

    future_fixtures = [
        {
            'player_id': player_id,
            'fixture_id': fixture['id'],
            'kickoff_time': fixture['kickoff_time'],
            'is_home': fixture['is_home'],
            'team_h': fixture['team_h'],
            'team_a': fixture['team_a'],
            'difficulty': fixture['difficulty']
        }
        for fixture in player_data['fixtures'] if not fixture['finished']
    ]

    match_history = [
        {
            'player_id': player_id,
            'own_team': player_ids.loc[player_ids['id'] == player_id, 'team_code'].values[0],
            'fixture_id': match['fixture'],
            'minutes': match['minutes'],
            'goals_scored': match['goals_scored'],
            'assists': match['assists'],
            'kickoff_time': match['kickoff_time'],
            'total_points': match['total_points'],
            'yellow_cards': match['yellow_cards'],
            'penalties_saved': match['penalties_saved'],
            'saves': match['saves'],
            'bps': match['bps'],
            'own_goals': match['own_goals'],
            'clean_sheets': match['clean_sheets'],
            'opponent_team': match['opponent_team'],
            'ict_index': match['ict_index']
        }
        for match in player_data['history']
    ]
    return future_fixtures, match_history

# Step 4: Fetch Data for All Players Concurrently
def fetch_all_player_data(player_ids):
    all_fixtures_data = []
    all_players_data = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_player_data_from_summary, player_id) for player_id in player_ids['id']]
        for future in futures:
            try:
                future_fixtures, match_history = future.result()
                all_fixtures_data.extend(future_fixtures)
                all_players_data.extend(match_history)
            except Exception as e:
                print(f"Error fetching data: {e}")
    return all_fixtures_data, all_players_data

# Step 5: Create DataFrames and merge team data
def create_dataframes(all_fixtures_data, all_players_data, player_ids):
    future_fixtures_df = pd.DataFrame(all_fixtures_data)
    match_df = pd.DataFrame(all_players_data)
    future_fixtures_df = future_fixtures_df.merge(player_ids[['id', 'full_name', 'position']], left_on='player_id', right_on='id', how='left')
    match_df = match_df.merge(player_ids[['id', 'full_name', 'position', 'form', 'points_per_game']], left_on='player_id', right_on='id', how='left')
    return future_fixtures_df, match_df

# Step 6: Create difficulty mapping from future fixtures
def create_difficulty_mapping(future_fixtures_df):
    difficulty_mapping = {}
    for _, row in future_fixtures_df.iterrows():
        home_team = row['team_h']
        away_team = row['team_a']
        difficulty = row['difficulty']
        difficulty_mapping[(home_team, away_team)] = difficulty
    difficulty_df = pd.DataFrame(list(difficulty_mapping.items()), columns=['team_pair', 'difficulty'])
    difficulty_df[['home_team', 'away_team']] = pd.DataFrame(difficulty_df['team_pair'].tolist(), index=difficulty_df.index)
    return difficulty_df.drop(columns=['team_pair'])

# Step 7: Map difficulties to match_df
def map_difficulties(match_df, difficulty_df):
    match_df = pd.merge(match_df, difficulty_df, left_on=['own_team', 'opponent_team'], right_on=['home_team', 'away_team'], how='left')
    match_df = pd.merge(match_df, difficulty_df, left_on=['opponent_team', 'own_team'], right_on=['home_team', 'away_team'], suffixes=('', '_reverse'), how='left')
    match_df['match_difficulty'] = match_df['difficulty'].fillna(match_df['difficulty_reverse'])
    return match_df.drop(columns=['difficulty', 'difficulty_reverse', 'home_team', 'away_team'])

# New function to get most recent matchup stats if available
def get_last_matchup_stats(player_id, opponent_team, match_df):
    matchup_data = match_df[(match_df['player_id'] == player_id) & (match_df['opponent_team'] == opponent_team)]
    if not matchup_data.empty:
        # Get the most recent match against this opponent
        last_match = matchup_data.sort_values(by='kickoff_time', ascending=False).iloc[0]
        return last_match
    return None