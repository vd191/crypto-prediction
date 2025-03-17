import pandas as pd # type: ignore
import joblib # type: ignore
# from scripts.data_preprocessing import preprocess_data
from scripts.feature_engineering import add_ict_features

def predict():
    # Step 1: Preprocess new data
    # preprocess_data()

    # Step 2: Create features
    # create_features()

    # Step 3: Load the trained model
    model = joblib.load("models/random_forest.pkl")

    # Step 4: Add ICT features
    df = pd.read_csv("data/processed/data_to_predict.csv")
    df = add_ict_features(df)   

    # Step 5: Predict the signal
    X = df[['Close', 'Volume', 'bullish_ob', 'bearish_ob',
        'bullish_fvg', 'bearish_fvg',
        'HH', 'LL', 'uptrend', 'downtrend',
        'london_session', 'ny_session']]
    latest_signal = model.predict(X.iloc[[-1]])  # Predict for the latest row

    # Map signal to action
    if latest_signal == 1:
        action = "Buy"
    elif latest_signal == -1:
        action = "Sell"
    else:
        action = "Hold"

    print(f"Predicted Action: {action}")
    return action