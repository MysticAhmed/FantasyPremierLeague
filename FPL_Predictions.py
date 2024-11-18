import streamlit as st
from tabs import *
from utils import *
from Kits import *
import requests
import re
# Initialize session state
if 'formation' not in st.session_state:
    st.session_state.formation = "5-4-1"


goalie_future_fixture, defender_future_fixture, midfielder_fixtures_df, forward_fixtures_df, all_players = load_data()
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

with st.sidebar:
    st.markdown("""
    <style>
    .chat-bubble {
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        width: fit-content;
        max-width: 70%;
        word-wrap: break-word;
    }
    .user-bubble {
        background-color: #1E90FF;
        color: white;
        align-self: flex-end;
        margin-left: auto;
    }
    .assistant-bubble {
        background-color: #F0F0F0;
        color: black;
        align-self: flex-start;
        margin-right: auto;
    }
    .chat-container {
        display: flex;
        flex-direction: column-reverse; /* Reverse order of messages */
        overflow-y: auto;
        max-height: 400px;  /* Adjust height based on your preference */
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 10px;
    }
    .chat-input-container {
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hi! Type a player's name to get their predicted points!"}
        ]

    # Chat input box at the top
    with st.container():
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        prompt = st.chat_input("Type in a player name...")
        st.markdown('</div>', unsafe_allow_html=True)

        if prompt:
            # Add user's message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            response = "Sorry, I couldn't find information about that player."  # Default response

            # Extract tokens (words) from the prompt
            tokens_in_prompt = set(re.findall(r'\w+', prompt.lower()))  # Tokenizes the prompt into lowercase words

            # Match player name from the prompt
            for _, row in all_players.iterrows():
                player_name_tokens = set(re.findall(r'\w+', row['player_name'].lower()))  # Tokenize the player's name
                # Check if any token in the player's name matches a token in the prompt
                if player_name_tokens & tokens_in_prompt:  # Set intersection to find matching tokens
                    response = (
                        f"{row['player_name']} is predicted to have: {math.ceil(row['prediction'])} points 🏆 "
                    )
                    break

            # Add assistant's response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": response})

    # Chat history display below input box
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in reversed(st.session_state.chat_history):  # Reverse the display order of messages
        if message["role"] == "user":
            st.markdown(f"<div class='chat-bubble user-bubble'><b>User:</b> {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble assistant-bubble'><b>Assistant:</b> {message['content']}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
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