import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title='View Data',
    page_icon='',
    layout='wide'
)

# Define the display_data function
def display_data(selected_feature_type):
    data = df_train
    if selected_feature_type == 'All Features':
        data = data
    elif selected_feature_type == 'Numeric Features':
        data = data.select_dtypes(include='number')
    elif selected_feature_type == 'Categorical Features':
        data = data.select_dtypes(exclude='number')
    elif selected_feature_type == 'Demographic Features':
        data = data[['gender', 'SeniorCitizen', 'Partner', 'Dependents']]
    elif selected_feature_type == 'Service Features':
        data = data[['tenure', 'PhoneService', 'MultipleLines', 'InternetService',
                       'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                       'TechSupport', 'StreamingTV', 'StreamingMovies']]
    elif selected_feature_type == 'Cost Features':
        data = data[['Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']]
    elif selected_feature_type == 'Target Variable [Churn]':
        data = data[['Churn']]
    else:
        data = pd.DataFrame()  # Default empty DataFrame

    st.table(data)

# Check if the user is logged in
if 'name' not in st.session_state:
    st.error("You need to log in to access this page.")
else:
    with st.sidebar:
        st.title("Logout")
        if st.button("Logout"):
            del st.session_state["name"]
            st.success("You have been successfully logged out.")
            
    # Load datasets
    df_1st = pd.read_csv('./Dataset/df_churn_first_3000.csv')
    df_2nd = pd.read_csv('./Dataset/LP2_Telco-churn-second-2000.csv')
    df_train = pd.concat([df_1st, df_2nd], ignore_index=True)

    # Main UI layout
    st.subheader('Data used for Training Models')

    selected_feature_type = st.selectbox("Please select group of features or Target",
                                         options=['All Features', 'Numeric Features',
                                                  'Categorical Features', 'Demographic Features',
                                                  'Service Features', 'Cost Features', 'Target Variable [Churn]'],
                                         key='selected_features', index=0)

    display_data(selected_feature_type)

    st.write(st.session_state)