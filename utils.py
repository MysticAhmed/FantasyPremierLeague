import pandas as pd
import requests
import streamlit as st
import os
response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
data = response.json()
positions = {1: "Goalkeeper", 2: "Defender", 3: "Midfielder", 4: "Forward"}
player_id_to_name = {player['id']: player['web_name'] for player in data['elements']}
player_name_to_id = {player['web_name']: player['id'] for player in data['elements']}
player_id_to_value = {player['id']: player['now_cost'] for player in data['elements']}
player_id_to_position = {player['id']: positions[player['element_type']] for player in data['elements']}
player_id_to_team_code = {player['id']: player['team_code'] for player in data['elements']}
team_names = {team['code']: team['name'] for team in data['teams']}

def get_player_name(player_id, player_id_to_name):
    return player_id_to_name.get(player_id, "Unknown Player")
def get_player_id(name, player_name_to_id):
    return player_name_to_id.get(name, "Unknown Player") 
def get_player_position(player_id, player_id_to_position):
    return player_id_to_position.get(player_id, "Unknown Position")

def get_player_value(player_id, player_id_to_value):
    return player_id_to_value.get(player_id, "Unknown Position")


def get_team_code(player_id, player_id_to_team_code):
    return player_id_to_team_code.get(player_id, "Unknown Team")

def load_data():
    
    # Get the directory where the script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct paths using os.path.join for cross-platform compatibility
    csv_dir = os.path.join(current_dir, 'CSV_Files')
    
    try:
        # Load future fixtures data from CSV
        goalie_future_fixture = pd.read_csv(os.path.join(csv_dir, 'goalie_predictions.csv'))
        defender_future_fixture = pd.read_csv(os.path.join(csv_dir, 'defender_predictions.csv'))
        midfielder_fixtures_df = pd.read_csv(os.path.join(csv_dir, 'midfielder_predictions.csv'))
        forward_fixtures_df = pd.read_csv(os.path.join(csv_dir, 'forward_predictions.csv'))

        all_players = pd.concat([goalie_future_fixture, defender_future_fixture, midfielder_fixtures_df, forward_fixtures_df])
        # Create a new column in all_players to replace player_id with player_name
        all_players['player_name'] = all_players['player_id'].map(player_id_to_name)

        return goalie_future_fixture, defender_future_fixture, midfielder_fixtures_df, forward_fixtures_df, all_players
    
    except FileNotFoundError as e:
        st.error(f"""
        CSV files not found. Please ensure the following files exist in the CSV_Files directory:
        - goalie_predictions.csv
        - defender_predictions.csv
        - midfielder_predictions.csv
        - forward_predictions.csv
        
        Error: {str(e)}
        """)
        # Return empty DataFrames as fallback
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
def player_for_value(dataset, value):
    dataset = dataset.sort_values(by='prediction', ascending=False)
    player_status_map = {player['id']: player['chance_of_playing_next_round'] for player in data['elements']}
    for _, row in dataset.iterrows():
        player_status = player_status_map.get(row['player_id'], 100)
        if player_status == None:
            player_status = 100

        if player_status > 50 and get_player_value(row['player_id'], player_id_to_value)/10 <= value:

            return f"I recommend <span style='color: maroon;'>{get_player_name(row['player_id'], player_id_to_name)}</span> from <span style='color: blue;'> {team_names.get(get_team_code(row['player_id'], player_id_to_team_code), player_id_to_team_code)}</span>"
    return "I could not find a suitable player with that value"


