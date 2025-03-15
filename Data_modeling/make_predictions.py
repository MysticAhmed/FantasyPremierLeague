import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def make_predictions(data, model, position):
    """
    Makes predictions using the trained models and adds them to future_fixtures_df.

    Args:
        prediction_data: DataFrame with features for prediction.
        goalie_model: Trained model for goalkeepers.
        defender_model: Trained model for defenders.
        midfielder_model: Trained model for midfielders.
        forward_model: Trained model for forwards.
    """
    player_id = data['player_id']
    data = data.drop(columns=['player_id'])
    # Reorder the columns to match the order during training
    if position == 'goalkeeper':
        data = data[['penalties_saved', 'saves', 'clean_sheets', 'minutes', 'bps', 'form', 'match_difficulty', 'points_per_game', 'ict_index']]  # Adjust column order
    elif position == 'defender':
        data = data[['saves', 'clean_sheets', 'own_goals', 'bps', 'minutes', 'form', 'match_difficulty', 'points_per_game', 'ict_index']]  # Adjust column order
    elif position == 'midfielder':
        data = data[['goals_scored', 'assists', 'bps', 'minutes', 'form', 'match_difficulty', 'points_per_game', 'ict_index']]  # Adjust column order
    elif position == 'forward':
        data = data[['goals_scored', 'assists', 'bps', 'minutes', 'form', 'match_difficulty', 'points_per_game', 'ict_index']]  # Adjust column order
    
    prediction = model.predict(data)
    data['prediction'] = prediction
    data['player_id'] = player_id

    return data