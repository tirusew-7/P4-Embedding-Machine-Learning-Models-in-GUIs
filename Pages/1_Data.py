import streamlit as st
import pyodbc
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title='View Data',
    page_icon='',
    layout='wide'
)

# Function to handle database connection
@st.cache_resource(show_spinner='Connecting to Database ...')
def initialize_connection():
    try:
        return pyodbc.connect(
            "DRIVER={SQL Server};SERVER="
            + st.secrets['SERVER']
            + ";DATABASE="
            + st.secrets['DATABASE']
            + ";UID="
            + st.secrets['UID']
            + ";PWD="
            + st.secrets['PWD']
        )
    except Exception as e:
        st.error(f"Error connecting to the database: {str(e)}")
        return None

# Check if the user is logged in
if 'name' not in st.session_state:
    st.error("You need to log in to access this page.")
else:
    # Establish database connection
    conn = initialize_connection()

    with st.sidebar:
        st.title("Logout")
        if st.button("Logout"):
            del st.session_state["name"]
            st.success("You have been successfully logged out.")

    # Function to query the database
    @st.cache_data()
    def query_database(query):
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            df = pd.DataFrame.from_records(data=rows, columns=[column[0] for column in cur.description])
        return df

    # Function to load CSV data
    @st.cache_data()
    def load_csv_data(file_path):
        df = pd.read_csv(file_path)
        return df

    # Specify the path to your CSV file
    csv_file_path = './Dataset/LP2_Telco-churn-second-2000.csv'
    df_2nd = load_csv_data(csv_file_path)

    # Load data from the database
    df_1st = query_database("SELECT * FROM LP2_Telco_Churn_first_3000")

    # Function to display data based on selected feature type
    def display_data(selected_feature_type):
        if selected_feature_type == 'All Features':
            data = pd.concat([df_1st, df_2nd], ignore_index=True)
        elif selected_feature_type == 'Numeric Features':
            data = df_1st.select_dtypes(include='number')
        elif selected_feature_type == 'Categorical Features':
            data = df_1st.select_dtypes(exclude='number')
        elif selected_feature_type == 'Demographic Features':
            data = df_1st[['gender', 'SeniorCitizen', 'Partner', 'Dependents']]
        elif selected_feature_type == 'Service Features':
            data = df_1st[['tenure', 'PhoneService', 'MultipleLines', 'InternetService',
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
