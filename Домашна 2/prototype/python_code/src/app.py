from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime

app = Flask(__name__)

def load_data():

    df = pd.read_csv('mse_historical_data.csv', encoding='utf-8')
    df['Датум'] = pd.to_datetime(df['Датум'], format='%d.%m.%Y')
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter', methods=['GET'])
def filter_data():
    stock_code = request.args.get('stockCode')
    from_date = request.args.get('dateFrom')
    to_date = request.args.get('dateTo')

    print(f"Filter Parameters: stock_code={stock_code}, from_date={from_date}, to_date={to_date}")

    existing_df = load_data()


    filtered_df = existing_df[
        (existing_df['Код на издавач'] == stock_code) &
        (existing_df['Датум'] >= pd.to_datetime(from_date, format='%d.%m.%Y')) &
        (existing_df['Датум'] <= pd.to_datetime(to_date, format='%d.%m.%Y'))
        ]


    data = filtered_df.values.tolist()


    return render_template('table.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)

