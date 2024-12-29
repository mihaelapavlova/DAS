from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(df, fastperiod=12, slowperiod=26, signalperiod=9):
    ema_fast = df['close'].ewm(span=fastperiod, min_periods=fastperiod).mean()
    ema_slow = df['close'].ewm(span=slowperiod, min_periods=slowperiod).mean()
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signalperiod, min_periods=signalperiod).mean()
    macd_hist = macd - macd_signal
    return macd, macd_signal, macd_hist

def calculate_stochastic(df, period=14):
    low_min = df['low'].rolling(window=period).min()
    high_max = df['high'].rolling(window=period).max()
    stochastic = 100 * ((df['close'] - low_min) / (high_max - low_min))
    return stochastic

def calculate_cci(df, period=20):
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    moving_avg = typical_price.rolling(window=period).mean()
    mad = (typical_price - moving_avg).abs().rolling(window=period).mean()
    cci = (typical_price - moving_avg) / (0.015 * mad)
    return cci

def calculate_atr(df, period=14):
    df['H-L'] = df['high'] - df['low']
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    atr = df['TR'].rolling(window=period).mean()
    return atr

def calculate_sma(df, window=10):
    return df['close'].rolling(window=window).mean()

def calculate_ema(df, span=10):
    return df['close'].ewm(span=span, adjust=False).mean()

def calculate_wma(df, window=10):
    weights = np.arange(1, window + 1)
    return df['close'].rolling(window=window).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)

def calculate_hma(df, period=14):
    half_length = period // 2
    sqrt_length = int(np.sqrt(period))
    wma_half = calculate_wma(df, window=half_length)
    wma_full = calculate_wma(df, window=period)
    hull_ma = calculate_wma(pd.DataFrame({'close': 2 * wma_half - wma_full}), window=sqrt_length)
    return hull_ma[0]

def calculate_vwap(df):
    vwap = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
    return vwap

# Signal generation logic

def generate_signal(df, period=14):
    last_row = df.iloc[-1]
    rsi = last_row[f'RSI_{period}']
    if rsi < 30:
        rsi_signal = 'Buy'
    elif rsi > 70:
        rsi_signal = 'Sell'
    else:
        rsi_signal = 'Hold'

    macd_hist = last_row[f'MACD_hist_{period}']
    if macd_hist > 0:
        macd_signal = 'Buy'
    elif macd_hist < 0:
        macd_signal = 'Sell'
    else:
        macd_signal = 'Hold'

    stochastic = last_row[f'Stochastic_{period}']
    if stochastic < 20:
        stochastic_signal = 'Buy'
    elif stochastic > 80:
        stochastic_signal = 'Sell'
    else:
        stochastic_signal = 'Hold'

    cci = last_row[f'CCI_{period}']
    if cci > 100:
        cci_signal = 'Sell'
    elif cci < -100:
        cci_signal = 'Buy'
    else:
        cci_signal = 'Hold'

    atr = last_row[f'ATR_{period}']
    if atr > 1.5:
        atr_signal = 'Sell'
    else:
        atr_signal = 'Buy'

    sma_10 = last_row[f'SMA_{period}']
    sma_50 = last_row['SMA_50']
    ema_10 = last_row[f'EMA_{period}']
    wma_10 = last_row[f'WMA_{period}']
    hma_14 = last_row[f'HMA_{period}']
    vwap = last_row[f'VWAP_{period}']

    if sma_10 > sma_50 and ema_10 > sma_50 and wma_10 > sma_50 and hma_14 > sma_50 and vwap > sma_50:
        ma_signal = 'Buy'
    else:
        ma_signal = 'Sell'

    if rsi_signal == 'Buy' and macd_signal == 'Buy' and ma_signal == 'Buy':
        final_signal = 'Buy'
    elif rsi_signal == 'Sell' and macd_signal == 'Sell' and ma_signal == 'Sell':
        final_signal = 'Sell'
    else:
        final_signal = 'Hold'

    return final_signal

# Sentiment analysis functions

def analyze_sentiment(csv_data):
    if not csv_data or len(csv_data) == 0:
        return 0  # No sentiment data, return neutral score
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(csv_data)
    return sentiment['compound']

def generate_recommendation(score):
    if score > 0.05:
        return "BUY"
    elif score < -0.05:
        return "SELL"
    else:
        return "HOLD"

# Loading data from CSV

def load_data_from_csv(file_path='mse_historical_data.csv'):
    df = pd.read_csv(file_path, encoding='utf-8')
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')  # Ensure date is in datetime format
    return df

# API routes

@app.route('/generate_signal', methods=['POST'])
def generate_signal_api():
    data = request.get_json()
    df = pd.DataFrame(data)
    periods = [5, 10, 14, 20, 50]
    time_frames = ["1_day", "1_week", "1_month"]
    results = {}

    for time_frame in time_frames:
        # Filter data based on time frame
        if time_frame == "1_day":
            df_filtered = df[df['date'] > pd.Timestamp.now() - pd.Timedelta(days=1)]
        elif time_frame == "1_week":
            df_filtered = df[df['date'] > pd.Timestamp.now() - pd.Timedelta(weeks=1)]
        elif time_frame == "1_month":
            df_filtered = df[df['date'] > pd.Timestamp.now() - pd.Timedelta(weeks=4)]

        for period in periods:
            # Calculate all indicators for this specific time_frame and period
            df[f'RSI_{period}'] = calculate_rsi(df_filtered, period=period)
            df[f'MACD_{period}'], df[f'MACD_signal_{period}'], df[f'MACD_hist_{period}'] = calculate_macd(df_filtered)
            df[f'Stochastic_{period}'] = calculate_stochastic(df_filtered, period=period)
            df[f'CCI_{period}'] = calculate_cci(df_filtered, period=period)
            df[f'ATR_{period}'] = calculate_atr(df_filtered, period=period)
            df[f'SMA_{period}'] = calculate_sma(df_filtered, window=period)
            df[f'EMA_{period}'] = calculate_ema(df_filtered, span=period)
            df[f'WMA_{period}'] = calculate_wma(df_filtered, window=period)
            df[f'HMA_{period}'] = calculate_hma(df_filtered, period=period)
            df[f'VWAP_{period}'] = calculate_vwap(df_filtered)

        final_signal = generate_signal(df_filtered)  # Generate the final signal for the filtered data
        results[time_frame] = final_signal

    return jsonify(results)

@app.route('/analyze', methods=['GET'])
def analyze_company():
    df = load_data_from_csv('mse_historical_data.csv')
    sentiment_score = analyze_sentiment(df['news'].iloc[0])  # Example for sentiment analysis
    recommendation = generate_recommendation(sentiment_score)
    return jsonify({"recommendation": recommendation})

if __name__ == '__main__':
    app.run(debug=True)


