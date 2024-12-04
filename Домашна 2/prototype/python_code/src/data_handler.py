import pandas as pd
import os
from config import historical_records_file

def load_data():
    if os.path.exists(historical_records_file):
        df = pd.read_csv(historical_records_file, dayfirst=True)
        df['Датум'] = pd.to_datetime(df['Датум'], errors='coerce', format='%d.%m.%Y')
        df = df.dropna(subset=['Датум'])
        df['Датум'] = df['Датум'].dt.strftime('%d.%m.%Y')
        return df
    return pd.DataFrame()

def save_data(data, existing_df):
    if data:
        df = pd.DataFrame(data, columns=['Код на издавач', 'Датум', 'Цена на последна трансакција', 'Мак.', 'Мин.',
                                         'Просечна цена', '%пром.', 'Количина', 'Промет во БЕСТ во денари',
                                         'Вкупен промет во денари'])
        df['Датум'] = pd.to_datetime(df['Датум'], format='%d.%m.%Y')
        df['Датум'] = df['Датум'].dt.strftime('%d.%m.%Y')
        combined_df = pd.concat([existing_df, df], ignore_index=True).drop_duplicates(
            subset=['Код на издавач', 'Датум'])
        combined_df.to_csv(historical_records_file, index=False, encoding='utf-8-sig')
        print(f"Data saved to {historical_records_file}")
