import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def make_predictions(data, model):
    player_id = data['player_id']
    data = data.drop(columns=['player_id'])
    prediction = model.predict(data)
    data['prediction'] = prediction
    data['player_id'] = player_id
    return data