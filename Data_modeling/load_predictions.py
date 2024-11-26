import os

def load_predictions(goalie, defender, midfielder, forward):
    base_path = 'CSV_Files'
    files = {
        "forward_predictions.csv": forward,
        "midfielder_predictions.csv": midfielder,
        "defender_predictions.csv": defender,
        "goalie_predictions.csv": goalie
    }
    
    for file_name, df in files.items():
        file_path = os.path.join(base_path, file_name)
        df.to_csv(file_path, index=False)
        if os.path.exists(file_path):
            print(f"{file_name} was successfully written.")
        else:
            print(f"Failed to write {file_name}.")
