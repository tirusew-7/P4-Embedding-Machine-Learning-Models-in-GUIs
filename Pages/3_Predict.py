
import streamlit as st
import joblib 
import imblearn  
import pandas as pd

model1_filename = "model1.joblib"
model2_filename = "model2.joblib"

model = joblib.load('path_to_your_model.pkl')

st.title('Customer Churn Prediction')
st.write('Please provide the following information:')

tenure = st.number_input('Tenure (months)', min_value=0)
monthly_charges = st.number_input('Monthly Charges', min_value=0.0)
total_charges = st.number_input('Total Charges', min_value=0.0)

user_data = pd.DataFrame({
    'SeniorCitizen_1': [1 if st.checkbox("Senior Citizen") else 0],
    'Partner_Yes': [1 if st.checkbox("Partner") else 0],
    'Dependents_Yes': [1 if st.checkbox("Dependents") else 0],
    'PhoneService_Yes': [1 if st.checkbox("Phone Service") else 0],
    'MultipleLines_No phone service': [0],
    'MultipleLines_Yes': [1 if st.checkbox("Multiple Lines") else 0],
    'InternetService_Fiber optic': [1 if st.checkbox("Fiber Optic Internet") else 0],
    'InternetService_No': [0],
    'OnlineSecurity_Yes': [1 if st.checkbox("Online Security") else 0],
    'OnlineBackup_Yes': [1 if st.checkbox("Online Backup") else 0],
    'DeviceProtection_Yes': [1 if st.checkbox("Device Protection") else 0],
    'TechSupport_Yes': [1 if st.checkbox("Tech Support") else 0],
    'StreamingTV_Yes': [1 if st.checkbox("Streaming TV") else 0],
    'StreamingMovies_Yes': [1 if st.checkbox("Streaming Movies") else 0],
    'Contract_One year': [1 if st.checkbox("One Year Contract") else 0],
    'Contract_Two year': [1 if st.checkbox("Two Year Contract") else 0],
    'PaperlessBilling_Yes': [1 if st.checkbox("Paperless Billing") else 0],
    'PaymentMethod_Credit card (automatic)': [0],
    'PaymentMethod_Electronic check': [1 if st.checkbox("Electronic Check") else 0],
    'PaymentMethod_Mailed check': [1 if st.checkbox("Mailed Check") else 0],
    'tenure': [tenure],
    'MonthlyCharges': [monthly_charges],
    'TotalCharges': [total_charges]
})

prediction = model.predict(user_data)

st.write(f'The predicted churn status is: {"Churn" if prediction[0] == 1 else "No Churn"}')
