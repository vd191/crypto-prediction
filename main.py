# Main script to run the entire pipeline

# from scripts.data_collection import fetch_data
# from scripts.data_preprocessing import preprocess_data
from scripts.feature_engineering import create_features
# from scripts.train_model import train_model
# from scripts.backtest import backtest_strategy
from scripts.predict import predict

def main():
    # Step 1: Fetch data
    # fetch_data()
    
    # Step 2: Preprocess data
    # preprocess_data()
    
    # Step 3: Feature engineering
    create_features()
    
    # Step 4: Train model
    # train_model()
    
    # Step 5: Backtest strategy
    # backtest_strategy()

    # Step 6: Predict
    predict()

if __name__ == "__main__":
    main()