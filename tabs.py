import streamlit as st
import math
import pandas as pd
from utils import *
from Kits import find_kit

def own_team_predictions(goalie_future_fixture, defender_future_fixture, midfielder_fixtures_df, forward_fixtures_df, data, positions, team_names):
    st.markdown(f"<h1 style='text-align: center; color: white; font-size : 30px;'>See how many points your current team may score!</h1>", unsafe_allow_html=True)
    
    # Initialize dictionaries for players
    all_goalies = {}
    all_defenders = {}
    all_midfielders = {}
    all_forwards = {}

    # Populate the dictionaries with player details
    for player in data['elements']:
        player_id = player['id']
        player_data = {
            'web_name': player['web_name'],
            'id': player_id,
            'team_code': player['team_code']
        }

        if positions[player['element_type']] == "Goalkeeper" and player_id in set(goalie_future_fixture['player_id']):
            all_goalies[player_id] = player_data
        elif positions[player['element_type']] == "Defender" and player_id in set(defender_future_fixture['player_id']):
            all_defenders[player_id] = player_data
        elif positions[player['element_type']] == "Midfielder" and player_id in set(midfielder_fixtures_df['player_id']):
            all_midfielders[player_id] = player_data
        elif positions[player['element_type']] == "Forward" and player_id in set(forward_fixtures_df['player_id']):
            all_forwards[player_id] = player_data

    page_text = """
    <style>
    [data-testid="stSelectbox"]{
        color : "#FFFFFF"
    }
    </style>
    """
    st.markdown(page_text, unsafe_allow_html=True)
    # Formation input with a unique key
    formation = st.selectbox(
        "Pick a formation",
        ("5-4-1", "5-3-2", "5-2-3", "5-1-4", "4-4-2", "4-3-3", "4-2-4", "4-1-5", "3-5-2", "3-4-3", "3-3-4", "3-2-5", "3-1-6", "2-5-3", "2-4-4", "2-3-5", "2-2-6"),
        key="formation2"
    )

    # Parse the formation input to determine the number of players per position
    try:
        defen = int(formation[0])
        mid = int(formation[2])
        forw = int(formation[4])
    except (ValueError, IndexError):
        st.error("Please enter a valid formation format (e.g., 4-4-2)")
        defen = mid = forw = 0

    def position_selectbox(position, player_dict, key_prefix):
        # Add placeholder option
        options = [{"label": "Select a player", "id": None}] + [
            {
                "label": f"{player_data['web_name']} ({team_names[player_data['team_code']]})",
                "id": player_id,
            }
            for player_id, player_data in player_dict.items()
        ]

        # Default index to 0 for placeholder
        selected = st.selectbox(
            f"{position}", options, format_func=lambda option: option["label"], key=f"{key_prefix}_selectbox"
        )
        return selected["id"] if selected and selected["id"] else None


    def calculate_points(players_df):
        return sum(math.ceil(player['prediction']) for _, player in players_df.iterrows())

    # Dropdowns for each position
    selected_goalie = position_selectbox("Goalkeeper", all_goalies, "goalie")
    selected_defenders = [position_selectbox(f"Defender {i+1}", all_defenders, f"defender_{i}") for i in range(defen)]
    selected_midfielders = [position_selectbox(f"Midfielder {i+1}", all_midfielders, f"midfielder_{i}") for i in range(mid)]
    selected_forwards = [position_selectbox(f"Forward {i+1}", all_forwards, f"forward_{i}") for i in range(forw)]

    # Convert selected player names to their IDs
    selected_goalie_id = selected_goalie
    selected_defender_ids = [player for player in selected_defenders if player]
    selected_midfielder_ids = [player for player in selected_midfielders if player]
    selected_forward_ids = [player for player in selected_forwards if player]

    # Filter each CSV by the selected player IDs
    selected_goalie_df = goalie_future_fixture[goalie_future_fixture['player_id'] == selected_goalie_id] if selected_goalie_id else pd.DataFrame()
    selected_defenders_df = defender_future_fixture[defender_future_fixture['player_id'].isin(selected_defender_ids)]
    selected_midfielders_df = midfielder_fixtures_df[midfielder_fixtures_df['player_id'].isin(selected_midfielder_ids)]
    selected_forwards_df = forward_fixtures_df[forward_fixtures_df['player_id'].isin(selected_forward_ids)]

    # Function to display a player's information in a column
    def display_player_in_selected_players(column, player):
        player_id = player["player_id"]
        team_code = get_team_code(player_id, player_id_to_team_code)
        player_name = get_player_name(player_id, player_id_to_name)
        player_position = get_player_position(player_id, player_id_to_position)
        player_value = get_player_value(player_id, player_id_to_value)
        team_name = team_names.get(team_code)
        jersey_url = find_kit(team_name)

        with column:
            st.markdown(
                f"<p style='text-align: center; color: yellow; font-size: 17px; margin: 1px 0;'>{player_position}: {player_name}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align: center; font-size: 17px; margin: 1px 0; color: white;'>Team: {team_name}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div style='display: flex; justify-content: center;'>"
                f"<img src='{jersey_url}' alt='Jersey' style='width: 60px; height: auto; border-radius: 5px;'>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align: center; font-size: 17px; margin: 1px 0; color: lime;'>💲: {player_value / 10} M</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align: center; color: orange; font-size: 17px; margin: 1px 0;'>Predicted Points 🏆: {math.ceil(player['prediction'])}</p>",
                unsafe_allow_html=True,
            )
            st.divider()
        
    def display_players_by_position2(goalkeepers, defenders, midfielders, forwards):
        for _, players in [("Goalkeepers", goalkeepers), ("Defenders", defenders), ("Midfielders", midfielders), ("Forwards", forwards)]:
            if not players.empty:
                cols = st.columns(len(players))
                for col, (_, player) in zip(cols, players.iterrows()):
                    display_player_in_selected_players(col, player)

    if st.button("Generate Predictions for Selected Players"):
        selected_players = pd.concat([selected_goalie_df, selected_defenders_df, selected_midfielders_df, selected_forwards_df])
        predicted_points = calculate_points(selected_players)
        display_players_by_position2(selected_goalie_df, selected_defenders_df, selected_midfielders_df, selected_forwards_df)
        st.markdown(
            f"<h1 style='text-align: center; color: pink; font-size : 30px; margin: 1px 0;'>Total Predicted Points: {predicted_points}</h1>",
            unsafe_allow_html=True,
        )




def dream_team(upcoming_gameweek, team_names, goalie_future_fixture, defender_future_fixture, midfielder_fixtures_df, forward_fixtures_df):
    # Initialize these locally instead of using global variables
    predicted_points = 0
    total_price = 0

    st.markdown(f"<h1 style='text-align: center; color: white; font-size : 30px;'>Best Starting XI for {upcoming_gameweek}</h1>", unsafe_allow_html=True)
    # Formation input with a unique key
    formation1 = st.selectbox("Pick a formation", ("5-3-2", "4-4-2","4-3-3", "3-5-2", "3-4-3"), key="formation1")

    # Parse the formation input to determine the number of players per position
    try:
        defen = int(formation1[0])
        mid = int(formation1[2])
        forw = int(formation1[4])
    except (ValueError, IndexError):
        st.error("Please enter a valid formation format (e.g., 4-4-2)")
        defen = mid = forw = 0  # Default to zero to avoid additional errors

    # Constants
    MAX_PLAYERS_PER_TEAM = 3
    SQUAD_REQUIREMENTS = {"Goalkeeper": 2, "Defender": 5, "Midfielder": 5, "Forward": 3}

    # Initialize counters
    team_counts = {}
    position_counts = {position: 0 for position in SQUAD_REQUIREMENTS}
    knocked = st.toggle("Include Injured Players")
    player_status_map = {player['id']: player['chance_of_playing_next_round'] for player in data['elements']}
    def filter_players_with_combined_limit(players, max_needed, team_counts, position_counts, position):
        """
        Filters players based on team and position limits while considering their status from the FPL API.
        """
        # Sort players by prediction in descending order
        sorted_players = players.sort_values(by='prediction', ascending=False)
        selected_players = []

        # Create a mapping of player_id to status using the API data
        

        for _, player in sorted_players.iterrows():
            player_id = player['player_id']
            team_name = team_names.get(get_team_code(player_id, player_id_to_team_code))
            # Check if the player's status is active (e.g., "a" for available in the FPL API)
            player_status = player_status_map.get(player_id, 100)
            if player_status == None:
                player_status = 100
            if knocked:
                # Enforce constraints: team limit, position limit, and player availability
                if (
                    team_counts.get(team_name, 0) < MAX_PLAYERS_PER_TEAM and
                    position_counts[position] < max_needed and
                    player_status > 50  # Only include available players
                ):
                    selected_players.append(player)
                    team_counts[team_name] = team_counts.get(team_name, 0) + 1
                    position_counts[position] += 1
            else:
                if (
                    team_counts.get(team_name, 0) < MAX_PLAYERS_PER_TEAM and
                    position_counts[position] < max_needed and
                    player_status == 100  # Only include available players
                ):
                    selected_players.append(player)
                    team_counts[team_name] = team_counts.get(team_name, 0) + 1
                    position_counts[position] += 1

            # Stop if the required number of players is reached
            if len(selected_players) == max_needed:
                break

        return pd.DataFrame(selected_players)

    # Dynamically select the Starting XI
    starting_goalkeepers = filter_players_with_combined_limit(goalie_future_fixture, 1, team_counts, position_counts, "Goalkeeper")
    starting_defenders = filter_players_with_combined_limit(defender_future_fixture, defen, team_counts, position_counts, "Defender")
    starting_midfielders = filter_players_with_combined_limit(midfielder_fixtures_df, mid, team_counts, position_counts, "Midfielder")
    starting_forwards = filter_players_with_combined_limit(forward_fixtures_df, forw, team_counts, position_counts, "Forward")

    # Combine the Starting XI into a single DataFrame
    starting_xi_display = pd.concat([starting_goalkeepers, starting_defenders, starting_midfielders, starting_forwards])

    #Reset count for bench
    position_counts = {position: 0 for position in SQUAD_REQUIREMENTS}
    # Function to calculate total bench points
    def calculate_bench_points(config):
        """
        Calculate total points for the bench players in a configuration,
        rounding each player's prediction individually before summing.
        """
        total_points = 0
        for role, players_df in config.items():
            if not players_df.empty and 'prediction' in players_df.columns:
                total_points += players_df['prediction'].apply(round).sum()
        return total_points


    # Bench selection configurations
    bench_goalkeeper_1 = filter_players_with_combined_limit(
        goalie_future_fixture[~goalie_future_fixture['player_id'].isin(starting_goalkeepers['player_id'])],
        1, team_counts.copy(), position_counts.copy(), "Goalkeeper"
    )
    bench_defender_1 = filter_players_with_combined_limit(
        defender_future_fixture[~defender_future_fixture['player_id'].isin(starting_defenders['player_id'])],
        2, team_counts.copy(), position_counts.copy(), "Defender"
    )
    bench_midfielder_1 = filter_players_with_combined_limit(
        midfielder_fixtures_df[~midfielder_fixtures_df['player_id'].isin(starting_midfielders['player_id'])],
        1, team_counts.copy(), position_counts.copy(), "Midfielder"
    )

    bench_goalkeeper_2 = filter_players_with_combined_limit(
        goalie_future_fixture[~goalie_future_fixture['player_id'].isin(starting_goalkeepers['player_id'])],
        1, team_counts.copy(), position_counts.copy(), "Goalkeeper"
    )
    bench_defender_2 = filter_players_with_combined_limit(
        defender_future_fixture[~defender_future_fixture['player_id'].isin(starting_defenders['player_id'])],
        1, team_counts.copy(), position_counts.copy(), "Defender"
    )
    bench_midfielder_2 = filter_players_with_combined_limit(
        midfielder_fixtures_df[~midfielder_fixtures_df['player_id'].isin(starting_midfielders['player_id'])],
        2, team_counts.copy(), position_counts.copy(), "Midfielder"
    )

    # Define configurations
    config_1 = {
        "bench_goalkeeper": bench_goalkeeper_1,
        "bench_defender": bench_defender_1,
        "bench_midfielder": bench_midfielder_1,
    }

    config_2 = {
        "bench_goalkeeper": bench_goalkeeper_2,
        "bench_midfielder": bench_midfielder_2,
        "bench_defender": bench_defender_2,
    }

    # Calculate total points for each configuration
    config_1_points = calculate_bench_points(config_1)
    config_2_points = calculate_bench_points(config_2)


    # Filter additional players for the bench to meet FPL requirements
    if defen == 5:
        bench_goalkeeper = filter_players_with_combined_limit(goalie_future_fixture[~goalie_future_fixture['player_id'].isin(starting_goalkeepers['player_id'])], 1, team_counts, position_counts, "Goalkeeper")
        bench_midfielder = filter_players_with_combined_limit(midfielder_fixtures_df[~midfielder_fixtures_df['player_id'].isin(starting_midfielders['player_id'])], 2, team_counts, position_counts, "Midfielder")
        bench_forward = filter_players_with_combined_limit(forward_fixtures_df[~forward_fixtures_df['player_id'].isin(starting_forwards['player_id'])], 1, team_counts, position_counts, "Forward")
        bench_display = pd.concat([bench_goalkeeper, bench_midfielder, bench_forward])
    elif mid == 5:
        bench_goalkeeper = filter_players_with_combined_limit(goalie_future_fixture[~goalie_future_fixture['player_id'].isin(starting_goalkeepers['player_id'])], 1, team_counts, position_counts, "Goalkeeper")
        bench_defender = filter_players_with_combined_limit(defender_future_fixture[~defender_future_fixture['player_id'].isin(starting_defenders['player_id'])], 2, team_counts, position_counts, "Defender")
        bench_forward = filter_players_with_combined_limit(forward_fixtures_df[~forward_fixtures_df['player_id'].isin(starting_forwards['player_id'])], 1, team_counts, position_counts, "Forward")
        bench_display = pd.concat([bench_goalkeeper, bench_defender , bench_forward])
    elif forw == 3:
        if config_1_points >= config_2_points:
            bench_goalkeeper = config_1["bench_goalkeeper"]
            bench_defender = config_1["bench_defender"]
            bench_midfielder = config_1["bench_midfielder"]
            bench_display = pd.concat([bench_goalkeeper, bench_defender, bench_midfielder])
        else:
            bench_goalkeeper = config_2["bench_goalkeeper"]
            bench_defender = config_2["bench_defender"]
            bench_midfielder = config_2["bench_midfielder"]
            bench_display = pd.concat([bench_goalkeeper, bench_defender, bench_midfielder])
    else:
        bench_goalkeeper = filter_players_with_combined_limit(goalie_future_fixture[~goalie_future_fixture['player_id'].isin(starting_xi_display['player_id'])], 1, team_counts, position_counts, "Goalkeeper")
        bench_midfielder = filter_players_with_combined_limit(midfielder_fixtures_df[~midfielder_fixtures_df['player_id'].isin(starting_xi_display['player_id'])], 1, team_counts, position_counts, "Midfielder")
        bench_forward = filter_players_with_combined_limit(forward_fixtures_df[~forward_fixtures_df['player_id'].isin(starting_xi_display['player_id'])], 1, team_counts, position_counts, "Forward")
        bench_defender = filter_players_with_combined_limit(defender_future_fixture[~defender_future_fixture['player_id'].isin(starting_xi_display['player_id'])], 1, team_counts, position_counts, "Defender")
        bench_display = pd.concat([bench_goalkeeper, bench_defender, bench_midfielder, bench_forward])


    # Convert player_id columns to sets for quick membership checking
    starting_xi_ids = set(starting_xi_display['player_id'])
    # Function to check if a player is in the starting XI or bench
    def is_in_starting_xi(player_id):
        return player_id in starting_xi_ids

    # Function to display a player's information in a column
    def display_player_in_column(column, player):
        nonlocal predicted_points, total_price
        player_id = player["player_id"]
        team_code = get_team_code(player_id, player_id_to_team_code)
        player_name = get_player_name(player_id, player_id_to_name)
        player_position = get_player_position(player_id, player_id_to_position)
        player_value = get_player_value(player_id, player_id_to_value)
        team_name = team_names.get(team_code)
        jersey_url = find_kit(team_name)
        player_status = player_status_map.get(player_id, 100)
        if player_status == None:
            player_status = 100

        with column:
            st.markdown(
                f"<p style='text-align: center; color: yellow; font-size: 17px; margin: 1px 0;'>{player_position}: {player_name}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align: center; font-size: 17px; margin: 1px 0; color: white;'>Team: {team_name}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div style='display: flex; justify-content: center;'>"
                f"<img src='{jersey_url}' alt='Jersey' style='width: 60px; height: auto; border-radius: 5px;'>"
                f"</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align: center; font-size: 17px; margin: 1px 0; color: lime;'>💲: {player_value / 10} M</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align: center; color: orange; font-size: 17px; margin: 1px 0;'>Predicted Points 🏆: {math.ceil(player['prediction'])}</p>",
                unsafe_allow_html=True,
            )
            if player_status < 100:
                st.markdown(
                f"<p style='text-align: center; color: red; font-size: 17px; margin: 1px 0;'> ⚠️ Injured: {player_status}% chance of playing</p>",
                unsafe_allow_html=True,
            )
            st.divider()



        if is_in_starting_xi(player_id):
            predicted_points += math.ceil(player["prediction"])
        total_price += player_value

        
    st.markdown(f"<h2 style='text-align: center; color: white;'>Starting XI</h2>", unsafe_allow_html=True)
    # Display players by position, adding the is_bench argument for Bench section
    def display_players_by_position(goalkeepers, defenders, midfielders, forwards):

        for _, players in [("Goalkeepers", goalkeepers), ("Defenders", defenders), ("Midfielders", midfielders), ("Forwards", forwards)]:
            if len(players) > 0:
                cols = st.columns(len(players))
                for col, (_, player) in zip(cols, players.iterrows()):
                    display_player_in_column(col, player)

    # Separate Starting XI and Bench displays
    display_players_by_position(
        goalkeepers=starting_xi_display[starting_xi_display['player_id'].map(lambda x: get_player_position(x, player_id_to_position)) == "Goalkeeper"],
        defenders=starting_xi_display[starting_xi_display['player_id'].map(lambda x: get_player_position(x, player_id_to_position)) == "Defender"],
        midfielders=starting_xi_display[starting_xi_display['player_id'].map(lambda x: get_player_position(x, player_id_to_position)) == "Midfielder"],
        forwards=starting_xi_display[starting_xi_display['player_id'].map(lambda x: get_player_position(x, player_id_to_position)) == "Forward"]
)

    st.markdown(f"<h2 style='text-align: center; color: white;'>Bench</h2>", unsafe_allow_html=True)
    def display_bench_players_in_rows(bench_players):
        # Display bench players in rows of 4 without nested iteration
        if bench_players.empty:
            st.write("No bench players to display.")
            return
        num_bench_players = len(bench_players)
        players_per_row = 4

        for i in range(0, num_bench_players, players_per_row):
            row_players = bench_players.iloc[i:i + players_per_row]  # Select 4 players for each row
            cols = st.columns(min(players_per_row, len(row_players)))  # Create a column for each player in the row
            
            for col, (_, player) in zip(cols, row_players.iterrows()):
                display_player_in_column(col, player)


    display_bench_players_in_rows(bench_display)


    # Display total predicted points and price summary at the end
    st.markdown(f"<h1 style='text-align: center; color: pink; font-size : 30px;  margin: 1px 0;'>Total Predicted Points: {predicted_points}</h1>", unsafe_allow_html=True)
    if total_price / 10 > 100:
        st.markdown(f"<h1 style='text-align: center; color: red; font-size: 20px;  margin: 1px 0;'>This configuration exceeds the FPL 100M limit, choose wisely</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; color: green; font-size : 30px;  margin: 1px 0;'>Total Price: {total_price / 10}M</h1>", unsafe_allow_html=True)

    return predicted_points, total_price  # Return the values instead of using globals