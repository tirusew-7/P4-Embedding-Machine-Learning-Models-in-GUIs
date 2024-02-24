# Import necessary libraries
import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pyodbc
from streamlit_secrets import get_secret

# Function to fetch data from SQL Server
def fetch_data():
    # Fetch credentials from Streamlit secrets
    secrets = get_secret("my_secrets")

    # Connection details
    conn_str = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={secrets['servername']};DATABASE={secrets['databasename']};UID={secrets['user']};PWD={secrets['password']}"
    
    # SQL Query to fetch data from the specified table
    query = f"SELECT * FROM {secrets['tablename']}"

    # Fetch data from SQL Server and convert to DataFrame
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    df = pd.DataFrame([tuple(row) for row in rows], columns=[column[0] for column in cursor.description])
    conn.close()

    # Encode categorical variables using LabelEncoder
    le = LabelEncoder()
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = le.fit_transform(df[column])

    return df

# Create Data Page
def data_page():
    st.title("Data Page")

    # Fetch data from SQL Server
    data = fetch_data()

    # Display the fetched data
    st.dataframe(data)

# Run the app
if __name__ == "__main__":
    data_page()
