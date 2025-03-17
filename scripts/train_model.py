# Script to train ML models

import pandas as pd # type: ignore
from sklearn.ensemble import RandomForestClassifier # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.metrics import accuracy_score # type: ignore
import joblib # type: ignore

def train_model():
    # Load feature-rich data
    df = pd.read_csv("data/processed/features.csv")

    # Define features and target
    X = df[['Close', 'Volume', 'bullish_ob', 'bearish_ob',
        'bullish_fvg', 'bearish_fvg',
        'HH', 'LL', 'uptrend', 'downtrend',
        'london_session', 'ny_session']]
    y = (df['Close'].shift(-1) > df['Close']).astype(int)  # Buy (1) if price increases, else Sell (0)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Create results DataFrame with aligned indices
    results_df = pd.DataFrame(index=X.index)  # Use X.index to ensure alignment
    results_df['Close'] = df.loc[X.index, 'Close']
    
    # Make predictions on the entire dataset X
    results_df['Predicted_Signal'] = model.predict(X)
    results_df['Actual_Direction'] = y
    results_df['Correct_Prediction'] = (results_df['Predicted_Signal'] == results_df['Actual_Direction']).astype(int)
    
    # Add performance metrics
    results_df['Next_Close'] = df.loc[X.index, 'Close'].shift(-1)
    results_df['Price_Change'] = results_df['Next_Close'] - results_df['Close']
    results_df['Return'] = results_df['Price_Change'] / results_df['Close']
    results_df['Strategy_Return'] = results_df['Return'] * results_df['Predicted_Signal']
    
    # Calculate cumulative returns
    results_df['Cumulative_Return'] = (1 + results_df['Strategy_Return']).cumprod()
    
    # Save results
    results_df.to_csv("results/training_results.csv")
    print("\nTraining results saved to results/training_results.csv")
    
    # Print summary statistics
    correct_predictions = results_df['Correct_Prediction'].sum()
    total_predictions = len(results_df['Correct_Prediction'])
    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
    
    print(f"\nTraining Summary:")
    print(f"Total Predictions: {total_predictions}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Final Cumulative Return: {results_df['Cumulative_Return'].iloc[-1]:.2%}")
    
    # Feature importance
    feature_imp = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print("\nTop 5 Most Important Features:")
    print(feature_imp.head())
    
    # Save model
    joblib.dump(model, "models/random_forest.pkl")
    print("\nModel trained and saved to models/random_forest.pkl")