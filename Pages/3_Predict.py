import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import RandomOverSampler

# Define numerical and categorical columns
numerical_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
categorical_cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                     'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
                     'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod']

def make_pipeline(model):
    numerical_transformer = SimpleImputer(strategy='mean')  # Impute missing numerical values
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute missing categorical values
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])

    return Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])

@st.cache_resource(show_spinner='Forest Model Loading')
def load_forest_model():
    pipeline = joblib.load('models/RForest_model.joblib')
    return pipeline

@st.cache_resource(show_spinner='Regression Model Loading')
def load_regression_pipeline():
    pipeline = joblib.load('models/LRegression_model.joblib')
    return pipeline

def select_model():
    col1, col2 = st.columns(2)

    with col1:
        st.selectbox("Select Model", options=['Random Forest Model', 'Regression Model'], key='selected_model')
    
    with col2:
        pass

    if st.session_state['selected_model'] == 'Random Forest Model':
        pipeline = load_forest_model()  # Load Random Forest model
    else:
        pipeline = load_regression_pipeline()  # Load Regression model

    encoder = joblib.load('./models/encoder.joblib')

    return pipeline, encoder

def make_prediction(pipeline, encoder):
    gender = st.session_state['gender']
    senior_citizen = st.session_state['senior_citizen']
    partner = st.session_state['partner']
    dependents = st.session_state['dependents']
    tenure = st.session_state['tenure']
    phone_service = st.session_state['phone_service']
    multiple_lines = st.session_state['multiple_lines']
    internet_service = st.session_state['internet_service']
    online_security = st.session_state['online_security']
    online_backup = st.session_state['online_backup']
    device_protection = st.session_state['device_protection']
    tech_support = st.session_state['tech_support']
    streaming_tv = st.session_state['streaming_tv']
    streaming_movies = st.session_state['streaming_movies']
    contract = st.session_state['contract']
    paperless_billing = st.session_state['paperless_billing']
    payment_method = st.session_state['payment_method']
    monthly_charges = st.session_state['monthly_charges']
    total_charges = st.session_state['total_charges']

    columns = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 'MultipleLines',
               'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
               'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
               'MonthlyCharges', 'TotalCharges']

    data = [[gender, senior_citizen, partner, dependents, tenure, phone_service, multiple_lines, internet_service,
             online_security, online_backup, device_protection, tech_support, streaming_tv, streaming_movies,
             contract, paperless_billing, payment_method, monthly_charges, total_charges]]

    df = pd.DataFrame(data, columns=columns)

    # Make prediction using the pipeline
    pred = pipeline.predict(df)
    prediction = int(pred[0])
    prediction = encoder.inverse_transform([prediction])

    # Get Probabilities
    probability = pipeline.predict_proba(df)

    return prediction, probability

def display_form():
    loaded_model, encoder = select_model()

    if loaded_model is not None:
        col1, col2, col3 = st.columns(3)

        with st.form("Input Feature"):
            with col1:
                st.write("### Demographic Features")
                st.selectbox("Gender", key='gender', options=['Female', 'Male'])
                st.selectbox("Senior Citizen", key='senior_citizen', options=['Yes', 'No'])
                st.selectbox("Partner", key='partner', options=['Yes', 'No'])
                st.selectbox("Dependents", key='dependents', options=['Yes', 'No'])

            with col2:
                st.write("### Service Features")
                st.number_input("Tenure", key='tenure')
                st.selectbox("Phone Service", key='phone_service', options=['Yes', 'No'])
                st.selectbox("Multiple Lines", key='multiple_lines', options=['Yes', 'No'])
                st.selectbox("Internet Service", key='internet_service', options=['DSL', 'Fiber optic', 'No'])
                st.selectbox("Online Security", key='online_security', options=['Yes', 'No'])
                st.selectbox("Online Backup", key='online_backup', options=['Yes', 'No'])
                st.selectbox("Device Protection", key='device_protection', options=['Yes', 'No'])
                st.selectbox("Tech Support", key='tech_support', options=['Yes', 'No'])
                st.selectbox("Streaming TV", key='streaming_tv', options=['Yes', 'No'])
                st.selectbox("Streaming Movies", key='streaming_movies', options=['Yes', 'No'])
                              
            with col3:
                st.write("### Cost Related Features")
                st.selectbox("Contract", key='contract', options=['Month-to-month', 'One year', 'Two year'])
                st.selectbox("Paperless Billing", key='paperless_billing', options=['Yes', 'No'])
                st.selectbox("Payment Method", key='payment_method', options=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
                st.number_input("Monthly Charges", key='monthly_charges')
                st.number_input("Total Charges", key='total_charges')

            # Check for form submission outside the context manager
            if st.form_submit_button("Predict Churn"):
                prediction, probability = make_prediction(loaded_model, encoder)
                st.session_state['prediction'] = prediction
                st.session_state['probability'] = probability

if __name__ == "__main__":
    st.markdown("<h1 style='text-align: center;'>Customer Churn Prediction</h1>", unsafe_allow_html=True)
    display_form()

    if 'prediction' in st.session_state:
        st.markdown(f"<h2 style='text-align: center;'>Predicted Churn: **{st.session_state['prediction'][0]}**</h2>", unsafe_allow_html=True)
        st.write("Probability of Churn:", st.session_state['probability'][0][1])  # Assuming second element is churn probability