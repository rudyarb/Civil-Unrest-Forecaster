import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
import pandas as pd
import joblib
import os

INPUT_DATA_PATH = os.path.join(os.getcwd(),"Input")
input_file = os.path.join(INPUT_DATA_PATH, "unrest_hold_out.csv")
OUTPUT_DATA_PATH = os.path.join(os.getcwd(),"Output")

# Load model, preprocessor, and holdout set
model = joblib.load(os.path.join(OUTPUT_DATA_PATH,'rf_model.pkl'))
preprocessor = joblib.load(os.path.join(OUTPUT_DATA_PATH,'preprocessor.pkl'))
df_holdout = pd.read_csv(input_file, parse_dates=['month'])

# Features used by the model
features = ['gini_index_lag1','unemployment_rate_lag1','inflation_rate_lag1','media_sentiment_index_lag1','rainfall_deviation_lag1',
            'policy_instability_index_lag1','prior_unrest_count_lag1','population_density_lag1','food_price_index_lag1',
            'fuel_subsidy_cut_lag1','gov_approval_lag1','neighbor_unrest_prev_lag1',
            'rolling_unrest_3mo', 'month_num', 'months_since_unrest']

st.title("Civil Unrest Predictor")

# Region and month selectors
st.write("This interactive tool helps you estimate the risk of unrest events in different regions for the upcoming month. It uses historical data and machine learning to generate predictions. To get started, please select the month you would like to see the prediction for and region from the options below.")

regions = sorted(df_holdout['region_id'].unique(), key=lambda x: int(x[1:]))
months = sorted(df_holdout['month'].dt.strftime('%Y-%m').unique())

region = st.selectbox("Select a Region", regions)
month_str = st.selectbox("Select a Month for Prediction", months)
month = pd.to_datetime(month_str)

# Filter row
row = df_holdout[(df_holdout['region_id'] == region) & (df_holdout['month'] == month)]

if row.empty:
    st.warning("No data found for this region-month.")
else:
    X = row[features]
    X_processed = preprocessor.transform(X)
    pred = model.predict(X_processed)[0]
    prob = model.predict_proba(X_processed)[0][1]

    st.markdown(
        f"<h2>The chance of unrest occurring in Region <strong>{int(region[1:])}</strong> in the month {month.strftime('%Y-%m')} is <span style='color:red; font-weight:normal;'>{prob:.2%}</span>.</h2>",
        unsafe_allow_html=True
    )

# Info about prediction
st.subheader("How We Make This Prediction")

# Important features
st.write("View the most important features the model uses to make this prediction.")
# See all the most important features that are being considered by the model when making this prediction.

# Get importances
importances = model.feature_importances_
feature_names = ['gini_index_lag1', 'unemployment_rate_lag1', 'inflation_rate_lag1',
 'media_sentiment_index_lag1', 'rainfall_deviation_lag1',
 'policy_instability_index_lag1', 'prior_unrest_count_lag1',
 'population_density_lag1', 'food_price_index_lag1', 'fuel_subsidy_cut_lag1',
 'gov_approval_lag1', 'neighbor_unrest_prev_lag1', 'rolling_unrest_3mo',
 'months_since_unrest', 'fuel_subsidy_cut_lag1_0.0',
 'fuel_subsidy_cut_lag1_1.0', 'month_num_1', 'month_num_10', 'month_num_11',
 'month_num_12', 'month_num_2', 'month_num_3', 'month_num_4', 'month_num_5',
 'month_num_6', 'month_num_7', 'month_num_8', 'month_num_9']

# Sort importance in descending order
sorted_idx = np.argsort(importances)
sorted_importances = importances[sorted_idx]
sorted_features = np.array(feature_names)[sorted_idx]

# Plot
fig, ax = plt.subplots(figsize=(10, max(6, len(sorted_features) * 0.3)))
ax.barh(sorted_features, sorted_importances)
ax.set_title("Importance of Features")
ax.set_xlabel("Importance")
fig.tight_layout()

# Show in Streamlit
st.pyplot(fig)

# Evolution of indicators
st.subheader("Evolution of Features Over Time")

unrest_file = os.path.join(INPUT_DATA_PATH, "unrest.csv")

unrest_df = pd.read_csv(unrest_file, parse_dates=["month"])
unrest_df.sort_values(by=["region_id", "month"], inplace=True)

region_to_plot = region  # Plots whichever region the user selects

# Filter data
region_df = unrest_df[unrest_df["region_id"] == region_to_plot]

feature_list = ["prior_unrest_count", "unemployment_rate", "gov_approval", "food_price_index", "policy_instability_index"]

for metric in feature_list:
    # Plot trend
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(region_df["month"], region_df[f"{metric}"], marker="o", linestyle="-")
    ax.set_title(f"{metric.replace('_', ' ').title()} Trend in {region_to_plot}")
    ax.set_xlabel("Month")
    ax.set_ylabel(f"{metric.replace('_', ' ').title()}")
    ax.grid(True)
    st.pyplot(fig)
