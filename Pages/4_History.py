import streamlit as st
import pandas as pd
import os
from datetime import datetime

def show():
    st.title("History Page")
    show_history()

def show_history():
    if "history" in st.session_state:
        st.markdown("### Vodafone Churn Prediction History")
        input_features_df = st.session_state['df']
        history_df = pd.DataFrame(st.session_state["history"])
        History_df = pd.concat([history_df, input_features_df], axis=1)

        # Add columns for model, date, time, prediction, and probability
        History_df['Model-Chosen'] = History_df['model_name']
        History_df['Date'] = datetime.now().strftime("%Y-%m-%d")
        History_df['Time'] = datetime.now().strftime("%H:%M:%S")
        History_df['Prediction'] = History_df['prediction'].apply(lambda x: 'Yes' if x == 1 else 'No')
        History_df['Probability'] = History_df['probability']
        # Use the stored input features directly
        
        columns_to_drop = ['prediction', 'probability', 'model_name']
        History_df = History_df.drop(columns=columns_to_drop)
        new_column_order = ['Model-Chosen', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Prediction', 'Probability', 'Date', 'Time']
        History_df = History_df[new_column_order]

        # Save history dataframe to CSV including new columns
        save_to_csv(History_df)

        display_saved_file("History.csv")

        
    else:
        st.write("No previous history found.")

def save_to_csv(History_df):
    try:
        # Check if the file exists
        if os.path.isfile("History.csv"):
            # If it exists, append the new data to the file
            History_df.to_csv("History.csv", mode='a', header=False, index=False)
        else:
            # If it doesn't exist, create a new file
            History_df.to_csv("History.csv", index=False)
    except Exception as e:
        st.error(f"Error saving history to CSV: {e}")
def display_saved_file(file_path):
    try:
        saved_df = pd.read_csv(file_path)
        st.markdown(f"### Saved File: {file_path}")
        st.write(saved_df)
    except Exception as e:
        st.error(f"Error reading and displaying saved file: {e}")
def main():
    show_history()

if __name__ == "__main__":
    main()
