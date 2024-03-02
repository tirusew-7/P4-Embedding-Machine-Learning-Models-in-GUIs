import streamlit as st
import pandas as pd
import pyodbc
import toml
import os

@st.cache_resource
def connect_to_database():
    secrets_path = os.path.join(os.path.dirname(__file__), '..', '.streamlit', 'secrets.toml')
    try:
        secrets = toml.load(secrets_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: secrets.toml file not found at {secrets_path}")

    server = secrets['database']['server']
    database = secrets['database']['database']
    username = secrets['database']['username']
    password = secrets['database']['password']
    connection_string = f"DRIVER=SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"
    return pyodbc.connect(connection_string)

def list_tables():
    connection = connect_to_database()
    if connection is None:
        st.error("Error: Unable to connect to the database.")
        st.stop()

    cursor = connection.cursor()
    query = "SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_type = 'BASE TABLE';"
    cursor.execute(query)
    tables = cursor.fetchall()
    st.write("Tables in the database:")
    st.write([table[0] for table in tables])

def read_data(query):
    connection = connect_to_database()
    if connection is None:
        st.error("Error: Unable to connect to the database.")
        st.stop()

    cursor = connection.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    data = cursor.fetchall()
    return pd.DataFrame.from_records(data, columns=columns)

# Remove the direct invocation of list_tables() from the script
