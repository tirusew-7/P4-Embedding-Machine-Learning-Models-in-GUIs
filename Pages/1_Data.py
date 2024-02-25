# 1_Data.py

import streamlit as st
from database_utils import read_data

# Example SQL query
sql_query = "SELECT * FROM LP2_Telco_churn_first_3000;"

# Use the read_data function to fetch data from the database
result_df = read_data(sql_query)

# Display the data in the Streamlit app
st.write("Data from the database:")
st.write(result_df)
