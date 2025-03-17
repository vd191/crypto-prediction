# Script to backtest strategies

import pandas as pd # type: ignore
import joblib # type: ignore    

def backtest_strategy():
    # Load model and data
    model = joblib.load("models/random_forest.pkl")
    df = pd.read_csv("data/processed/features.csv")

    # Define features
    X = df[[
        'Close', 'Volume', 'bullish_ob', 'bearish_ob',
        'bullish_fvg', 'bearish_fvg',
        'HH', 'LL', 'uptrend', 'downtrend',
        'london_session', 'ny_session'
    ]].dropna()

    # Convert boolean columns to int
    bool_columns = ['bullish_ob', 'bearish_ob', 'bullish_fvg', 'bearish_fvg',
                   'HH', 'LL', 'uptrend', 'downtrend', 'london_session', 'ny_session']
    for col in bool_columns:
        X[col] = X[col].astype(int)

    # Create results DataFrame with aligned indices
    results_df = pd.DataFrame(index=X.index)
    results_df['Close'] = df.loc[X.index, 'Close']
    
    # Make predictions
    results_df['Predicted_Signal'] = model.predict(X)
    
    # Calculate actual price direction
    results_df['Actual_Direction'] = (df.loc[X.index, 'Close'].shift(-1) > df.loc[X.index, 'Close']).astype(int)
    results_df['Correct_Prediction'] = (results_df['Predicted_Signal'] == results_df['Actual_Direction']).astype(int)

    # Calculate returns
    results_df['Next_Close'] = df.loc[X.index, 'Close'].shift(-1)
    results_df['Price_Change'] = results_df['Next_Close'] - results_df['Close']
    results_df['Return'] = results_df['Price_Change'] / results_df['Close']
    results_df['Strategy_Return'] = results_df['Return'] * results_df['Predicted_Signal']
    
    # Calculate cumulative returns
    results_df['Cumulative_Return'] = (1 + results_df['Strategy_Return']).cumprod()

    # Save backtest results
    results_df.to_csv("results/backtest_results.csv")
    print("Backtest completed and results saved to results/backtest_results.csv")

    # Print performance metrics
    total_predictions = len(results_df)
    correct_predictions = results_df['Correct_Prediction'].sum()
    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
    
    print("\nBacktest Performance Metrics:")
    print(f"Total Predictions: {total_predictions}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Final Cumulative Return: {results_df['Cumulative_Return'].iloc[-1]:.2%}")
    
    # Additional trading metrics
    total_trades = len(results_df[results_df['Predicted_Signal'] != 0])
    winning_trades = len(results_df[
        (results_df['Predicted_Signal'] == 1) & (results_df['Return'] > 0) |
        (results_df['Predicted_Signal'] == -1) & (results_df['Return'] < 0)
    ])
    win_rate = winning_trades / total_trades if total_trades > 0 else 0
    
    print(f"\nTrading Metrics:")
    print(f"Total Trades: {total_trades}")
    print(f"Winning Trades: {winning_trades}")
    print(f"Win Rate: {win_rate:.2%}")
    
    # Calculate monthly returns
    if 'Date' in df.columns:
        results_df['Date'] = df.loc[X.index, 'Date']
        results_df['Date'] = pd.to_datetime(results_df['Date'])
        monthly_returns = results_df.set_index('Date')['Strategy_Return'].resample('M').sum()
        print("\nMonthly Returns:")
        print(monthly_returns.tail())