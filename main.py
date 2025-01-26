from Data_modeling.extract_api import *
import Data_modeling.clean_data as clean_data
import Data_modeling.performance_averages as performance_averages
import Data_modeling.prepare_data_for_prediction as prepare_data_for_prediction
import Data_modeling.make_predictions as make_predictions
import Data_modeling.load_predictions as load_predictions
import pickle
import requests
import logging
import azure.functions as func
import os


def main(mytimer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function started.')
    
    try:
        # Step 1: Get All Player Data and Team Data
        player_ids, teams = get_player_data()
        logging.info(f'Retrieved data for {len(player_ids)} players')
        
        teams_data = get_team_data(teams)
        logging.info('Team data retrieved successfully')

        # Step 2: Fetch data concurrently
        all_fixtures_data, all_players_data = fetch_all_player_data(player_ids)
        logging.info('Player and fixture data fetched successfully')

        # Step 3: Create DataFrames and merge team data
        future_fixtures_df, match_df = create_dataframes(all_fixtures_data, all_players_data, player_ids)

        # Step 4: Create difficulty mapping and map difficulties to match_df
        difficulty_df = create_difficulty_mapping(future_fixtures_df)
        match_df = map_difficulties(match_df, difficulty_df)

        #Cleans dataframe for training
        future_fixtures_df, match_df  = clean_data.clean_data(future_fixtures_df, match_df)

        #Prepares data for model prediction
        goalie_data, defender_data, midfielder_data, forward_data = prepare_data_for_prediction.prepare_data_for_prediction(future_fixtures_df, match_df)
        # Get the base path for the Azure Function
        base_path = os.getenv('AzureWebJobsScriptRoot')
        models_path = os.path.join(base_path, 'Models')

        # Load models using proper paths
        model_paths = {
            'forward': os.path.join(models_path, 'forward_model.pkl'),
            'midfielder': os.path.join(models_path, 'midfielder_model.pkl'),
            'defender': os.path.join(models_path, 'defender_model.pkl'),
            'goalie': os.path.join(models_path, 'goalie_model.pkl')
        }

        model_paths2 = {
            'forward': os.path.join(models_path, 'forward_model_NN.pkl'),
            'midfielder': os.path.join(models_path, 'midfielder_model_NN.pkl'),
            'defender': os.path.join(models_path, 'defender_model_NN.pkl'),
            'goalie': os.path.join(models_path, 'goalie_model_NN.pkl')
        }

        try:
            with open(model_paths['forward'], 'rb') as f:
                forward_model = pickle.load(f)
            with open(model_paths['defender'], 'rb') as f:
                defender_model = pickle.load(f)
            with open(model_paths['midfielder'], 'rb') as f:
                midfielder_model = pickle.load(f)
            with open(model_paths['goalie'], 'rb') as f:
                goalie_model = pickle.load(f)
        except Exception as e:
            logging.error(f'Error loading models: {str(e)}')
            raise

        #NN model
        try:
            with open(model_paths2['forward'], 'rb') as f:
                forward_model_NN = pickle.load(f)
            with open(model_paths2['defender'], 'rb') as f:
                defender_model_NN = pickle.load(f)
            with open(model_paths2['midfielder'], 'rb') as f:
                midfielder_model_NN = pickle.load(f)
            with open(model_paths2['goalie'], 'rb') as f:
                goalie_model_NN = pickle.load(f)
        except Exception as e:
            logging.error(f'Error loading models: {str(e)}')
            raise

        #Runs model on data for point prediction (currently using NN)
        goalie_predictions = make_predictions.make_predictions(goalie_data, goalie_model)
        defender_predictions = make_predictions.make_predictions(defender_data, defender_model)
        midfielder_predictions = make_predictions.make_predictions(midfielder_data, midfielder_model)
        forward_predictions = make_predictions.make_predictions(forward_data, forward_model)

        goalie_predictions_NN = make_predictions.make_predictions(goalie_data, goalie_model_NN)
        defender_predictions_NN = make_predictions.make_predictions(defender_data, defender_model_NN)
        midfielder_predictions_NN = make_predictions.make_predictions(midfielder_data, midfielder_model_NN)
        forward_predictions_NN = make_predictions.make_predictions(forward_data, forward_model_NN)

        '''# Log predictions
        logging.info(f'Generated predictions for:'
                    f'\n{len(goalie_predictions)} goalkeepers'
                    f'\n{len(defender_predictions)} defenders'
                    f'\n{len(midfielder_predictions)} midfielders'
                    f'\n{len(forward_predictions)} forwards')
        os.remove(r"CSV_Files/defender_predictions.csv")
        os.remove(r"CSV_Files/forward_predictions.csv")
        os.remove(r"CSV_Files/goalie_predictions.csv")
        os.remove(r"CSV_Files/midfielder_predictions.csv")'''
        
        # Save predictions
        load_predictions.load_predictions(goalie_predictions, defender_predictions, 
                        midfielder_predictions, forward_predictions)
        logging.info('Predictions saved successfully')

        # Log predictions
        logging.info(f'Generated predictions for:'
                    f'\n{len(goalie_predictions)} goalkeepers'
                    f'\n{len(defender_predictions)} defenders'
                    f'\n{len(midfielder_predictions)} midfielders'
                    f'\n{len(forward_predictions)} forwards')
        os.remove(r"CSV_Files/defender_predictions.csv")
        os.remove(r"CSV_Files/forward_predictions.csv")
        os.remove(r"CSV_Files/goalie_predictions.csv")
        os.remove(r"CSV_Files/midfielder_predictions.csv")
        
        # Save predictions
        load_predictions.load_predictions(goalie_predictions_NN, defender_predictions_NN, 
                        midfielder_predictions_NN, forward_predictions_NN)
        logging.info('Predictions saved successfully')

    except Exception as e:
        logging.error(f'Error in main function: {str(e)}')
        raise  # Re-raise the exception to mark the function as failed

    logging.info('Python timer trigger function completed successfully.')