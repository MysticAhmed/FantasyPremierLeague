import streamlit as st
from tabs import *
from utils import *
from Kits import *
import requests

# Initialize session state
if 'formation' not in st.session_state:
    st.session_state.formation = "5-4-1"

st.set_page_config(page_title= "Fantasy Premier Predictions",
                    page_icon= 'https://cdn-1.webcatalog.io/catalog/fantasy-premier-league/fantasy-premier-league-icon-filled-256.png?v=1675594263665',layout="wide", initial_sidebar_state="auto", menu_items=None)
goalie_future_fixture, defender_future_fixture, midfielder_fixtures_df, forward_fixtures_df = load_data()
# Create mappings for player_id to name and player_id to position
response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
data = response.json()
team_names = {team['code']: team['name'] for team in data['teams']}

gameweeks = data['events'] 
teams = data['teams']

#Get all team names in one dictionary for ease of access
team_names = {}
for team in teams:
    team_names[team['code']] = team['name']

#Find upcoming gameweek to update title
upcoming_gameweek = ""
for gameweek in gameweeks:
    if gameweek['finished'] == False:
        upcoming_gameweek = str(gameweek['name'])
        break

tab1, tab2 = st.tabs(["Dream Team", "Own Team Predictions"])

# Display the starting XI in Streamlit
with tab1:
    predicted_points, total_price = dream_team(
        upcoming_gameweek, 
        team_names, 
        goalie_future_fixture, 
        defender_future_fixture, 
        midfielder_fixtures_df, 
        forward_fixtures_df
    )

with tab2:
    own_team_predictions(
        goalie_future_fixture, 
        defender_future_fixture, 
        midfielder_fixtures_df, 
        forward_fixtures_df, 
        data, 
        positions,
        team_names
    )