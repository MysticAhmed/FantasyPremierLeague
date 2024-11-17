import pandas as pd
import requests

response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
data = response.json()
positions = {1: "Goalkeeper", 2: "Defender", 3: "Midfielder", 4: "Forward"}
player_id_to_name = {player['id']: player['web_name'] for player in data['elements']}
player_name_to_id = {player['web_name']: player['id'] for player in data['elements']}
player_id_to_value = {player['id']: player['now_cost'] for player in data['elements']}
player_id_to_position = {player['id']: positions[player['element_type']] for player in data['elements']}
player_id_to_team_code = {player['id']: player['team_code'] for player in data['elements']}

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
    # Load future fixtures data from CSV
    goalie_future_fixture = pd.read_csv(r'CSV_Files\goalie_predictions.csv')
    defender_future_fixture = pd.read_csv(r'CSV_Files\defender_predictions.csv')
    midfielder_fixtures_df = pd.read_csv(r'CSV_Files\midfielder_predictions.csv')
    forward_fixtures_df = pd.read_csv(r'CSV_Files\forward_predictions.csv')
    return goalie_future_fixture, defender_future_fixture, midfielder_fixtures_df, forward_fixtures_df