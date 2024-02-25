# Importing
import streamlit as st
import joblib  # Assuming joblib was used for model serialization
import imblearn  # Correct import statement
import pandas as pd

# Replace with actual model filenames and locations
model1_filename = "model1.joblib"
model2_filename = "model2.joblib"

# Load models using caching with appropriate error handling
@st.cache_resource
def load_model1():
    try:
        return joblib.load(model1_filename)
    except FileNotFoundError:
        st.error("Model 1 file not found!")
        return None

@st.cache_resource
def load_model2():
    try:
        return joblib.load(model2_filename)
    except FileNotFoundError:
        st.error("Model 2 file not found!")
        return None

# Select box for model selection
selected_model = st.selectbox("Select Model", ("Model 1", "Model 2"))

# Load the selected model and encoder (if applicable)
if selected_model == "Model 1":
    pipeline = load_model1()
    encoder = None  # Load encoder if required for Model 1
elif selected_model == "Model 2":
    pipeline = load_model2()
    encoder = None  # Load encoder if required for Model 2
else:
    st.error("Invalid model selection!")
    pipeline = None
    encoder = None

@st.cache(allow_output_mutation=False)
def make_prediction(column1, column2, column3):  # Adjust column names and types
    try:
        data = pd.DataFrame([[column1, column2, column3]], columns=[column1, column2, column3])  # Create DataFrame

        prediction = pipeline.predict(data)[0]  # Convert prediction to integer
        prediction = int(prediction)
        prediction_proba = pipeline.predict_proba(data)[0][prediction]  # Extract probability

        if encoder:
            prediction = encoder.inverse_transform([prediction])[0]  # Encode if necessary

        return prediction, prediction_proba
    except Exception as e:
        st.error(f"Prediction error: {e}")
        return None, None

# Clear prediction and probability before running make_prediction
if "prediction" not in st.session_state or "prediction_proba" not in st.session_state:
    st.session_state["prediction"] = None
    st.session_state["prediction_proba"] = None

# Display form and call make_prediction on button click
st.header("Prediction Form")
col1, col2, col3 = st.columns(3)  # Adjust column layout as needed
column1_value = col1.text_input("Column 1", key="column1")
column2_value = col2.text_input("Column 2", key="column2")
column3_value = col3.text_input("Column 3", key="column3")

if st.button("Make Prediction"):
    prediction, prediction_proba = make_prediction(column1_value, column2_value, column3_value)

    if prediction is not None and prediction_proba is not None:
        st.success(f"Prediction: {prediction}")
        st.write(f"Probability: {prediction_proba:.2f}")  # Format probability with 2 decimal places
    else:
        st.error("An error occurred while making the prediction.")

