# Script to create features

import pandas as pd # type: ignore
from ta import add_all_ta_features # type: ignore
from ta.volatility import AverageTrueRange # type: ignore

def create_features():
    # Load processed data
    df = pd.read_csv("data/processed/btc_1d_processed.csv")

    # Add technical indicators
    # df = add_all_ta_features(
    #     df, open="Open", high="High", low="Low", close="Close", volume="Volume"
    # )

    # Add ICT features
    df = add_ict_features(df)


    # Save feature-rich data
    df.to_csv("data/processed/features.csv", index=False)
    print("Features created and saved to data/processed/features.csv")


def identify_order_blocks(df, window=15):
    """Identify bullish and bearish order blocks"""
    df['High_prev'] = df['High'].shift(1)
    df['Low_prev'] = df['Low'].shift(1)
    df['Close_prev'] = df['Close'].shift(1)
    
    # Bullish Order Block (after a down move)
    df['bullish_ob'] = ((df['Low'] < df['Low'].shift(1)) & 
                       (df['High'].shift(-1) > df['High']))
    
    # Bearish Order Block (after an up move)
    df['bearish_ob'] = ((df['High'] > df['High'].shift(1)) & 
                       (df['Low'].shift(-1) < df['Low']))

def identify_fair_value_gaps(df):
    """Identify fair value gaps"""
    # Bullish FVG
    df['bullish_fvg'] = ((df['Low'] > df['High'].shift(1)) & 
                         (df['High'].shift(1) > df['Low'].shift(2)))
    
    # Bearish FVG
    df['bearish_fvg'] = ((df['High'] < df['Low'].shift(1)) & 
                         (df['Low'].shift(1) < df['High'].shift(2)))

def market_structure(df, window=10):
    """Identify market structure (higher highs, lower lows)"""
    df['HH'] = df['High'].rolling(window=window).max() == df['High']
    df['LL'] = df['Low'].rolling(window=window).min() == df['Low']
    
    # Trend identification
    df['uptrend'] = df['Close'] > df['Close'].rolling(window=window).mean()
    df['downtrend'] = df['Close'] < df['Close'].rolling(window=window).mean()


def add_ict_features(df):
    """Add ICT-specific features"""
    # Calculate ATR for volatility measurement
    atr = AverageTrueRange(df['High'], df['Low'], df['Close'], window=14)
    df['atr'] = atr.average_true_range()
    
    # Add Order Blocks
    identify_order_blocks(df)
    
    # Add Fair Value Gaps
    identify_fair_value_gaps(df)
    
    # Add Market Structure
    market_structure(df)
    
    # Add London/New York session indicators (assuming UTC timestamps)
    df['hour'] = pd.to_datetime(df.index).hour
    df['london_session'] = (df['hour'] >= 8) & (df['hour'] < 16)
    df['ny_session'] = (df['hour'] >= 13) & (df['hour'] < 21)
    
    return df