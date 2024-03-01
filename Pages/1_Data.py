import streamlit as st
import pyodbc
import pandas as pd

st.set_page_config(
    page_title='View Data',
    page_icon='',
    layout='wide'
)
st.title('Data from Database')

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

        df_1st = pd.DataFrame.from_records(data=rows, columns=[column[0] for column in cur.description])

    return df_1st


def select_all_features():
    query = "SELECT * FROM LP2_Telco_Churn_first_3000"
    df_1st = query_database(query)
    return df_1st


def select_numeric_features():
    query = "SELECT * FROM LP2_Telco_Churn_first_3000"
    df_1st = query_database(query)
    numeric_columns = df_1st.select_dtypes(include=['number']).columns
    df_numeric = df_1st[numeric_columns]
    return df_numeric


def select_categorical_features():
    query = "SELECT * FROM LP2_Telco_Churn_first_3000"
    df_1st = query_database(query)
    categorical_columns = df_1st.select_dtypes(exclude=['number']).columns
    df_categorical = df_1st[categorical_columns]
    return df_categorical


def select_demographic_features():
    query = "SELECT gender, SeniorCitizen, Partner, Dependents FROM LP2_Telco_Churn_first_3000"
    df_demographic = query_database(query)
    return df_demographic


def select_services_features():
    query = "SELECT tenure, PhoneService, MultipleLines, InternetService, OnlineSecurity, " \
            "OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies FROM LP2_Telco_Churn_first_3000"
    df_services = query_database(query)
    return df_services

def select_cost_features():
    query = "SELECT Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges FROM LP2_Telco_Churn_first_3000"
    df_cost = query_database(query)
    return df_cost


def select_target_variable():
    query = "SELECT Churn FROM LP2_Telco_Churn_first_3000"
    df_target = query_database(query)
    return df_target


if __name__ == "__main__":

    col1, col2 = st.columns(2)
    with col1:
        selected_feature_type = st.selectbox("Please select feature groups or Target", options=['All Features', 'Numeric Features', 
                                                                            'Categorical Features', 'Demographic Features', 'Service Features', 'Cost Features', 'Target Variable [Churn]'],
                                             key='selected_features')

    with col2:
        pass

    if selected_feature_type == 'All Features':
        data = select_all_features()
        st.dataframe(data)
    elif selected_feature_type == 'Numeric Features':
        numeric_data = select_numeric_features()
        st.dataframe(numeric_data)
    elif selected_feature_type == 'Categorical Features':
        categorical_data = select_categorical_features()
        st.dataframe(categorical_data)
    elif selected_feature_type == 'Demographic Features':
        demographic_data = select_demographic_features()
        st.dataframe(demographic_data)
    elif selected_feature_type == 'Service Features':
        services_data = select_services_features()
        st.dataframe(services_data)
    elif selected_feature_type == 'Cost Features':
        cost_data = select_cost_features()
        st.dataframe(cost_data)
    elif selected_feature_type == 'Target Variable [Churn]':
        target_data = select_target_variable()
        st.dataframe(target_data)

    st.write(st.session_state)

