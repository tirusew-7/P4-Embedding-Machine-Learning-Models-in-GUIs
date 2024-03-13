import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import os
from datetime import datetime

st.set_page_config(
    page_title='Churn Prediction',
    page_icon=':',
    layout='wide'
)
    
def show():
    st.title("Predict Page")
    # Your predict page content goes here
    st.write("This is the Predict Page content.")


# Loading logistic regression model
@st.cache_data(show_spinner='Logistic Regression Model Loading')
def logistic_regression_pipeline():
    model = joblib.load('./models/logistic_regression_pipeline.pkl')
    return model
 
# Loading random forest model
@st.cache_data(show_spinner='Random Forest Model Loading')
def random_forest_pipeline():
    model = joblib.load('./models/random_forest_pipeline.pkl')
    return model
 
# Loading encoder
@st.cache_resource(show_spinner='encoder Loading')
def load_encoder():
    encoder = joblib.load('./models/label_encoder.pkl')
    return encoder

# Selecting among the loaded Models
def select_model():
    col1, col2 = st.columns(2)
    with col1:
        model_name = st.selectbox('Select a Model', options=['Random Forest', 'Logistic Regression'])
        if model_name == 'Logistic Regression':
            model = logistic_regression_pipeline()  
        elif model_name == 'Random Forest':
            model = random_forest_pipeline()
        encoder = load_encoder()
    with col2:
        pass
    return model, encoder, model_name

#Making Prediction based on the loaded models and the loaded encoder
# Making Prediction based on the loaded models and the loaded encoder
def make_prediction(model_name, model, encoder):
    df = st.session_state['df']
    prediction = model.predict(df)
    probability = model.predict_proba(df)[:, 1].item()

    # Update history with user inputs and prediction, including timestamp
    if "history" not in st.session_state:
        st.session_state["history"] = []

    # Add columns for model, date, time, prediction, and probability
    new_entry = {
        "Model-Chosen": model_name,
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Prediction": 'Yes' if prediction[0] == 1 else 'No',
        "Probability": probability,
    }

    st.session_state["history"].append(new_entry)

    # Update session state with the latest prediction and probability
    st.session_state['prediction'] = prediction
    st.session_state['probability'] = probability

    return prediction

def predict_proba():
    probability = st.session_state.get('probability', None)
    if probability is not None:
        st.write(f"The probability of churn is: {probability:.2%}")

def predict():
    if 'prediction' not in st.session_state:
        st.session_state['prediction'] = None
    if 'probability' not in st.session_state:
        st.session_state['probability'] = None  # Initialize probability key
    model, encoder, model_name = select_model()
    with st.form('input feature'):
        col1, col2 = st.columns(2)
        with col1:
            # Add input fields and store values in input_features dictionary
            st.markdown('##### Demographic Features')
            gender = st.selectbox('gender', options=['Male', 'Female'], key='gender')
            SeniorCitizen = st.selectbox('SeniorCitizen', options=['Yes', 'No'], key='SeniorCitizen')
            Partner = st.selectbox('Partner', options=['Yes', 'No'], key='Partner')
            Dependents = st.selectbox('Dependents', options=['Yes', 'No'], key='Dependents')
            st.markdown('##### Service Features')
            tenure = st.number_input('tenure', min_value=0, max_value=71, step=1, key='tenure')  
            PhoneService = st.selectbox('PhoneService', options=['Yes', 'No'], key='PhoneService')
            MultipleLines = st.selectbox('MultipleLines', options=['Yes', 'No'], key='MultipleLines')
            InternetService = st.selectbox('InternetService', options=['Fiber optic', 'DSL'], key='InternetService')
            OnlineSecurity = st.selectbox('OnlineSecurity', options=['Yes', 'No'], key='OnlineSecurity')
        with col2:
            OnlineBackup = st.selectbox('OnlineBackup', options=['Yes', 'No'], key='OnlineBackup')
            DeviceProtection = st.selectbox('DeviceProtection', options=['Yes', 'No'], key='DeviceProtection')
            TechSupport = st.selectbox('TechSupport', options=['Yes', 'No'], key='TechSupport')
            StreamingTV = st.selectbox('StreamingTV', options=['Yes', 'No'], key='StreamingTV')
            StreamingMovies = st.selectbox('StreamingMovies', options=['Yes', 'No'], key='StreamingMovies')  
            st.markdown('##### Payment Features')
            Contract = st.selectbox('Contract', options=['Month-to-month', 'Two year', 'One year'], key='Contract')
            PaperlessBilling = st.selectbox('PaperlessBilling', options=['Yes', 'No'], key='PaperlessBilling')
            PaymentMethod = st.selectbox('PaymentMethod', options=['Electronic check', 'Credit card (automatic)', 'Mailed check', 'Bank transfer (automatic)'], key='PaymentMethod')
            MonthlyCharges = st.number_input('MonthlyCharges', min_value=0, key='MonthlyCharges')
            TotalCharges = st.number_input('TotalCharges', min_value=0, key='TotalCharges')

        input_features = pd.DataFrame({
            'gender': [gender],
            'SeniorCitizen': [SeniorCitizen],
            'Partner': [Partner],
            'Dependents': [Dependents],
            'tenure': [tenure],
            'PhoneService': [PhoneService],
            'MultipleLines': [MultipleLines],
            'InternetService': [InternetService],
            'OnlineSecurity': [OnlineSecurity],
            'OnlineBackup': [OnlineBackup],
            'DeviceProtection': [DeviceProtection],
            'TechSupport': [TechSupport],
            'StreamingTV': [StreamingTV],
            'StreamingMovies': [StreamingMovies],
            'Contract': [Contract],
            'PaperlessBilling': [PaperlessBilling],
            'PaymentMethod': [PaymentMethod],
            'MonthlyCharges': [MonthlyCharges],
            'TotalCharges': [TotalCharges]
        })

        # Store input features in the session state
        st.session_state['df'] = input_features

        st.form_submit_button('Predict Churn', on_click=make_prediction, kwargs=dict(model=model, encoder=encoder, model_name=model_name))
# Call the data function directly
if __name__ == '__main__':
    st.markdown('## Vodafom Churn Prediction Page')
    predict()
prediction = st.session_state['prediction']
if prediction is not None:
    if prediction[0] == 1:
        st.write(f"The customer will churn.")    
    else:
        st.write(f"The customer will not churn.")
    predict_proba()