import pandas as pd

def save_data(new_data, existing_df, filename='mse_historical_data.csv'):
    combined_data = pd.concat([existing_df, pd.DataFrame(new_data)], ignore_index=True)
    combined_data.to_csv(filename, index=False)
    return f"Податоците се успешно зачувани во {filename}."