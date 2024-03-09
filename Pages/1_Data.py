import streamlit as st
import pyodbc
import pandas as pd

st.set_page_config(
    page_title='View Data',
    page_icon='',
    layout='wide'
)
def show():
    st.title("Data Page")
    # Your data page content goes here
    st.write("This is the Data Page content.")
    
st.subheader('Data used for Training both from Database and CSV')

@st.cache_resource(show_spinner='Connecting to Database ...')
def initialize_connection():
    connection = pyodbc.connect(
        "DRIVER={SQL Server};SERVER="
        + st.secrets['SERVER']
        + ";DATABASE="
        + st.secrets['DATABASE']
        + ";UID="
        + st.secrets['UID']
        + ";PWD="
        + st.secrets['PWD']
    )
    return connection

conn = initialize_connection()

@st.cache_data()
def query_database(query):
    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()
        df = pd.DataFrame.from_records(data=rows, columns=[column[0] for column in cur.description])
    return df

def database_data():
    query = "SELECT * FROM LP2_Telco_Churn_first_3000"
    df = query_database(query)
    return df

# Data from CSV
@st.cache_data()
def load_csv_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Specify the path to your CSV file
csv_file_path = './Dataset/LP2_Telco-churn-second-2000.csv'
df_2nd = load_csv_data(csv_file_path)

# Load data from the database
df_1st = database_data()

# A function to show all the features
def get_all_features(df_train):
    return df_train

# A function to show numeric features
def select_numeric_features(df_train):
    numeric_columns = df_train.select_dtypes(include='number')
    return numeric_columns

# A function to show categorical features
def select_categorical_features(df_train):
    categorical_columns = df_train.select_dtypes(exclude='number')
    return categorical_columns

# A function to show demographic features
def select_demographic_features(df_train):
    df_demographic = df_train[['gender', 'SeniorCitizen', 'Partner', 'Dependents']]
    return df_demographic

# A function to show service features
def select_services_features(df_train):
    df_services = df_train[['tenure', 'PhoneService', 'MultipleLines', 'InternetService',
                            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                            'TechSupport', 'StreamingTV', 'StreamingMovies']]
    return df_services

# A function to show cost features
def select_cost_features(df_train):
    df_cost = df_train[['Contract', 'PaperlessBilling', 'PaymentMethod', 'MonthlyCharges', 'TotalCharges']]
    return df_cost

# A function to show target variable or Churn
def select_target_variable(df_train):
    df_target = df_train[['Churn']]
    return df_target

if __name__ == "__main__":
    col1, col2 = st.columns(2)
    with col1:
        selected_feature_type = st.selectbox("Please select group of features or Target",
                                             options=['All Features', 'Numeric Features',
                                                      'Categorical Features', 'Demographic Features',
                                                      'Service Features', 'Cost Features', 'Target Variable [Churn]'],
                                             key='selected_features')

    with col2:
        pass

    if selected_feature_type == 'All Features':
        data = get_all_features(pd.concat([df_1st, df_2nd], ignore_index=True))
        st.dataframe(data)
    elif selected_feature_type == 'Numeric Features':
        numeric_data = select_numeric_features(pd.concat([df_1st, df_2nd], ignore_index=True))
        st.dataframe(numeric_data)
    elif selected_feature_type == 'Categorical Features':
        categorical_data = select_categorical_features(pd.concat([df_1st, df_2nd], ignore_index=True))
        st.dataframe(categorical_data)
    elif selected_feature_type == 'Demographic Features':
        demographic_data = select_demographic_features(pd.concat([df_1st, df_2nd], ignore_index=True))
        st.dataframe(demographic_data)
    elif selected_feature_type == 'Service Features':
        services_data = select_services_features(pd.concat([df_1st, df_2nd], ignore_index=True))
        st.dataframe(services_data)
    elif selected_feature_type == 'Cost Features':
        cost_data = select_cost_features(pd.concat([df_1st, df_2nd], ignore_index=True))
        st.dataframe(cost_data)
    elif selected_feature_type == 'Target Variable [Churn]':
        target_data = select_target_variable(pd.concat([df_1st, df_2nd], ignore_index=True))
        st.dataframe(target_data)

    st.write(st.session_state)
