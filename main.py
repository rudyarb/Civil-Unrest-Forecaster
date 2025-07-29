from fastapi import FastAPI
import os
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up file paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = "Output/rf_model.pkl"
preprocessor_path = "Output/preprocessor.pkl"
file_path = "Input/unrest_hold_out.csv"

# Load model and preprocessor
model = joblib.load(model_path)
preprocessor = joblib.load(preprocessor_path)

@app.get("/")
def root():
    return {"message": "Welcome to the Unrest Prediction API!"}

@app.get("/predict")
def predict(region: str = "R3", month: str = "2032-01"):
    df_holdout = pd.read_csv(file_path, parse_dates=["month"])
    df_holdout['month_str'] = df_holdout['month'].dt.strftime('%Y-%m')
    month_str = pd.to_datetime(month).strftime('%Y-%m')

    row = df_holdout[(df_holdout['region_id'] == region) & (df_holdout['month_str'] == month_str)]

    if row.empty:
        return {"error": f"No data found for region {region} and month {month_str}"}

    features = [
        'gini_index_lag1','unemployment_rate_lag1','inflation_rate_lag1',
        'media_sentiment_index_lag1','rainfall_deviation_lag1',
        'policy_instability_index_lag1','prior_unrest_count_lag1',
        'population_density_lag1','food_price_index_lag1','fuel_subsidy_cut_lag1',
        'gov_approval_lag1','neighbor_unrest_prev_lag1','rolling_unrest_3mo',
        'month_num', 'months_since_unrest'
    ]

    X = row[features]
    X_processed = preprocessor.transform(X)

    prediction = model.predict(X_processed)[0]
    probability = model.predict_proba(X_processed)[0][1]  # probability of class 1 (unrest)

    return {
        "region": region,
        "month": month_str,
        "prediction": int(prediction),
        "probability_of_unrest": round(float(probability), 4)
    }
