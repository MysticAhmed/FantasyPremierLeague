import streamlit as st
from tabs import *
from utils import *
from Kits import *
import requests
import re
st.set_page_config("FPL Dream Team", page_icon = "https://rightanglecreative.co.uk/wp-content/uploads/2020/04/Blog-Post-260816-Premier-League-Logo-Thumbnail.jpg", layout = "wide", initial_sidebar_state= "auto", menu_items=  None)
# Initialize session state
page_bg_image = """
<style>
[data-testid="stAppViewContainer"]{
background-color:#0E1117}

.st-c1 {
    color: #FFFFFF;
}
</style>
"""
st.markdown(page_bg_image, unsafe_allow_html=True)
if 'formation' not in st.session_state:
    st.session_state.formation = "5-4-1"

# Inject CSS for changing the selectbox label color
    st.markdown(
    """
    <style>
    /* Change the color of the selectbox label */
    div.stSelectbox label {
        color: white !important;
    }

     /* Change the background color of the selectbox container */
    div[data-testid="stSelectbox"] .st-dk {
        background-color: rgb(38, 39, 48) !important; /* Change this to your desired color */
        border-radius: 5px !important; /* Optional: Smooth corners */
    }

    div > li.st-emotion-cache-doy61h.e1811lun0:first-child {
        background-color: rgb(38, 39, 48);
    }

    div[data-testid="stTooltipHoverTarget"]{
        background-color: rgb(38, 39, 48) !important; /* Change this to your desired color */
    }
    /* Change the background color of the dropdown options */
    ul[data-testid="stSelectboxVirtualDropdown"] {
        background-color: rgb(38, 39, 48) !important; /* Dropdown background color */
        border-radius: 5px !important; /* Optional: Smooth corners */
        border: 1px solid #ccc !important; /* Optional: Border styling */
    }

    #bui396val-1
    {
        background-color : rgb(38, 39, 48) !important
    }

    .st-emotion-cache-1ppef92:hover, .st-emotion-cache-1ppef92:active, .st-emotion-cache-1ppef92:focus-visible
    {
        background-color : rgb(38, 39, 48) !important
    }
    </style>
    """,
    unsafe_allow_html=True
    )

goalie_future_fixture, defender_future_fixture, midfielder_fixtures_df, forward_fixtures_df, all_players = load_data()
# Create mappings for player_id to name and player_id to position
response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
data = response.json()
team_names = {team['code']: team['name'] for team in data['teams']}

gameweeks = data['events'] 
teams = data['teams']

#Find upcoming gameweek to update title
upcoming_gameweek = ""
for gameweek in gameweeks:
    if gameweek['finished'] == False:
        upcoming_gameweek = str(gameweek['name'])
        break

tab1, tab2, tab3 = st.tabs(["Dream Team", "Own Team Predictions", "Ask your AI Manager!"])

with tab3:
    st.markdown("""
    <style>
    .chat-bubble {
        border-radius: 10px;
        color : gray;
        background-color : gray;
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
            {"role": "Manager", "content": "Hi! Type a player's name or ask for a player recommendation!"}
        ]

    # Chat input box at the top
    with st.container():
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        prompt = st.chat_input("Start with a name...")
        st.markdown('</div>', unsafe_allow_html=True)

        if prompt:
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            response = "Sorry, I couldn't find information about that player."  # Default response
            
            if "recommend" in prompt.lower():
                # Extract position and value using regular expressions
                position_match = re.search(r"(goalkeeper|defender|midfielder|forward)", prompt.lower())
                value_match = re.search(r"(\d+\.?\d*)m", prompt.lower())  # Look for a number followed by "M"

                # Extract the position and value
                position = position_match.group(1).capitalize() if position_match else None
                value = float(value_match.group(1)) if value_match else None
                if position == "Goalkeeper":
                    dataset = goalie_future_fixture
                elif position == "Defender":
                    dataset = defender_future_fixture
                elif position == "Midfielder":
                    dataset = midfielder_fixtures_df
                elif position == "Forward":
                    dataset = forward_fixtures_df
                # Run the recommendation function if both position and value are found
                if position and value:
                    recommendation = player_for_value(dataset, value)
                    response = recommendation  # Set the recommendation as the response
                else:
                    response = "Please provide both a valid position and a value (e.g., 'recommend a defender for 5.5M')."
            else:
                # Extract tokens (words) from the prompt
                tokens_in_prompt = set(re.findall(r'\w+', prompt.lower()))  # Tokenizes the prompt into lowercase words
                # Match player name from the prompt
                for _, row in all_players.iterrows():
                    player_id = row['player_id']
                    team_code = get_team_code(player_id, player_id_to_team_code)
                    player_name = get_player_name(player_id, player_id_to_name)
                    player_position = get_player_position(player_id, player_id_to_position)
                    player_value = get_player_value(player_id, player_id_to_value)
                    team_name = team_names.get(team_code)
                    player_name_tokens = set(re.findall(r'\w+', row['player_name'].lower()))  # Tokenize the player's name
                    # Check if any token in the player's name matches a token in the prompt
                    # Special edge case handling
                    if "m.salah" in prompt.lower():
                        player_id  = get_player_id("M.Salah", player_name_to_id)
                        team_code = get_team_code(player_id, player_id_to_team_code)
                        player_position = get_player_position(player_id, player_id_to_position)
                        player_value = get_player_value(player_id, player_id_to_value)
                        team_name = team_names.get(team_code)

                        response = (
                            f"With a value of <span style='color: green;'>{player_value / 10}M</span>, M.Salah plays as a {player_position} for <span style='color: red;'>{team_name}</span>. "
                            f"<p style='color: maroon;'>Predicted points: {math.ceil(row['prediction'])} 🏆</p>"
                        )

                    elif player_name_tokens & tokens_in_prompt :  # Set intersection to find matching tokens
                        response = (
                            f"With a value of <span style='color: green;'>{player_value / 10}M</span>, {row['player_name']} plays as a {player_position} for <span style='color: red;'>{team_name}</span>. "
                            f"<p style='color: maroon;'>Predicted points: {math.ceil(row['prediction'])} 🏆</p>"
                        )
                        break
            # Add assistant's response to chat history
            st.session_state.chat_history.append({"role": "Manager", "content": response})


    # Chat history display below input box
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in reversed(st.session_state.chat_history):  # Reverse the display order of messages
        if message["role"] == "user":
            st.markdown(f"<div class='chat-bubble user-bubble'><b>User:</b> {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble assistant-bubble'><b>AI Manager:</b> {message['content']}</div>", unsafe_allow_html=True)
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