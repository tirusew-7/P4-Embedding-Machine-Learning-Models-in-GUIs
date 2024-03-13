import streamlit as st
import pandas as pd
import yaml

# Load config file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

def save_config():
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file)

def authenticate(username, password):
    if username in config['credentials']['usernames']:
        stored_password = config['credentials']['usernames'][username]['password']
        if password == stored_password:
            return True
    return False

# Set page configuration
st.set_page_config(
    page_title='View Data',
    page_icon='',
    layout='wide'
)

# Check if the user is logged in
if 'name' not in st.session_state:
    st.sidebar.title("Login/Create Account")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if authenticate(username, password):
            st.session_state["name"] = username
            st.sidebar.success("Login successful.")
        else:
            st.sidebar.error("Invalid username or password. Please try again.")
    if st.sidebar.button("Create Account"):
        st.sidebar.success("Please enter your full name below to create an account.")
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        if new_username in config['credentials']['usernames']:
            st.sidebar.error("Username already exists. Please choose a different username.")
        else:
            config['credentials']['usernames'][new_username] = { 'email': '', 'logged_in': False, 'name': new_username, 'password': new_password}
            save_config()
            st.sidebar.success("Account created successfully. You can now log in.")

    st.warning("You need to log in or create an account to access the data.")

else:
    # Authenticate user login
    username = st.session_state['name']
    password = st.text_input("Password", type="password")
    if authenticate(username, password):
        st.success("Login successful.")
        file_path = '.Dataset\Telco-churn-last-2000.xlsx'
        # Function to load CSV data
        @st.cache
        def load_csv_data(file_path):
            df = pd.read_csv(file_path)
            return df

        # Specify the path to your CSV file
        csv_file_path = './Dataset/LP2_Telco-churn-second-2000.csv'
        df_2nd = load_csv_data(csv_file_path)

        # Load data from the database
        # Placeholder for loading data directly from the CSV file
        df_1st = pd.read_csv('./Dataset/Cleaned_data.csv')

        # Function to display data based on selected feature type
        def display_data(selected_feature_type):
            if selected_feature_type == 'All Features':
                data = pd.concat([df_1st, df_2nd], ignore_index=True)
            elif selected_feature_type == 'Numeric Features':
                data = df_1st.select_dtypes(include='number')
            elif selected_feature_type == 'Categorical Features':
                data = df_1st.select_dtypes(exclude='number')
            elif selected_feature_type == 'Demographic Features':
                data = df_1st[['Gender', 'SeniorCitizen', 'Partner', 'Dependents']]
            elif selected_feature_type == 'Service Features':
                data = df_1st[['Tenure', 'PhoneService', 'MultipleLines', 'InternetService',
                               'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                               'TechSupport', 'StreamingTV', 'StreamingMovies']]
            elif selected_feature_type == 'Cost Features':
                data = df_1st[['Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']]
            elif selected_feature_type == 'Target Variable [Churn]':
                data = df_1st[['Churn']]
            else:
                data = pd.DataFrame()  # Default empty DataFrame

            st.table(data)

        # Main UI layout
        st.title("Data Page")
        st.write("This is the Data Page content.")
        st.subheader('Data used for Training both from Database and CSV')

        selected_feature_type = st.selectbox("Please select group of features or Target",
                                             options=['All Features', 'Numeric Features',
                                                      'Categorical Features', 'Demographic Features',
                                                      'Service Features', 'Cost Features', 'Target Variable [Churn]'],
                                             key='selected_features', index=0)

        display_data(selected_feature_type)

        st.write(st.session_state)
    else:
        st.error("Invalid password. Please try again.")
