import streamlit as st
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math

st.set_page_config(
    page_title='View Data',
    page_icon='',
    layout='wide'
)


# Function to initialize the database connection
@st.cache_resource(show_spinner='Connecting to Database ...')
def initialize_connection():
    try:
        if 'conn' in globals():
            conn.close()  # Close the existing connection if it exists
    except Exception as e:
        st.error(f"Error closing connection: {e}")

    try:
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
    except Exception as e:
        st.error(f"Error establishing connection: {e}")

# Function to query the database
@st.cache_data()
def query_database(query):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            df = pd.DataFrame.from_records(data=rows, columns=[column[0] for column in cur.description])

        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")

# Function to select all features from the database
def select_all_features():
    query = "SELECT * FROM LP2_Telco_Churn_first_3000"
    df = query_database(query)
    return df

# Function to load CSV data
@st.cache_data()
def load_csv_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")

# Function to show the About Dashboard section
def show_about_dashboard():
    st.markdown("### About Dashboard")
    st.write('''
             This dashboard provides insights into Telco Churn data. 
             - Explores different visualizations and key performance indicators 
             - Helps to gain valuable information.
             - Provides a comprehensive overview of key metrics and 
             insights derived from the dataset.  
             - Includes a variety of visualizations to facilitate a quick understanding of the data. 
             - Users can quickly grasp the distribution of demographics such as gender, senior citizenship, and 
             partnership status.  
             - Represents important service-related information like 
             tenure, phone service, internet service, and contract details. 
             - Highlights crucial financial aspects, such as monthly 
             and total charges. 
             - identifies patterns and trends related to customer churn through visualizations that showcase the distribution of churned and non-churned 
             customers. 
             - Serves as centralized hub for exploring and gaining valuable 
             insights into the dataset, aiding in decision-making and strategy development.''')

# Function to show the Explore section
def generate_pie_chart(counts, labels, title):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff'])
    ax.set_title(title)
    return fig

def show_explore(df_train):
    st.markdown("### Exploratory Data Analysis ")
    st.sidebar.subheader("Filter among the following Options")

    numerical_columns = ['tenure', 'MonthlyCharges', 'TotalCharges']
    categorical_columns = ['gender', 'SeniorCitizen', 'PhoneService', 'StreamingMovies',
                                'Contract', 'PaperlessBilling', 'PaymentMethod', 'Churn']
    
    if categorical_columns:
        # Categorical variables
        for column in categorical_columns:
            if st.sidebar.checkbox(f'{column} Distribution'):
                column_counts = df_train[column].value_counts()
                if len(column_counts) <= 2:
                    # Bar chart for few unique values
                    fig, ax = plt.subplots()
                    ax.bar(column_counts.index, column_counts)
                    ax.set_title(f'Distribution of {column}')
                    ax.set_xlabel(column)
                    ax.set_ylabel('Count')
                    st.pyplot(fig)
                else:
                    # Pie chart for more unique values
                    fig, ax = plt.subplots()
                    ax.pie(column_counts, labels=column_counts.index, autopct='%1.1f%%',
                           startangle=90, colors=sns.color_palette('pastel'))
                    ax.set_title(f'Distribution of {column}')
                    st.pyplot(fig)

    if numerical_columns:
        # Numerical variables
        for column in numerical_columns:
            if st.sidebar.checkbox(f'{column} Distribution'):
                # Histogram for numerical values
                fig, ax = plt.subplots()
                ax.hist(df_train[column], bins=20, color=sns.color_palette('pastel')[0])
                ax.set_title(f'Distribution of {column}')
                ax.set_xlabel(column)
                ax.set_ylabel('Count')
                st.pyplot(fig)
        # Churn vs Numerical variables
    if numerical_columns:
        for column in numerical_columns:
            if st.sidebar.checkbox(f'{column} vs Churn'):
                fig, ax = plt.subplots()
                sns.histplot(data=df_train, x=column, hue='Churn', multiple='stack', bins=20, kde=True, palette='pastel')
                ax.set_title(f'{column} distribution by Churn')
                ax.set_xlabel(column)
                ax.set_ylabel('Count')
                st.pyplot(fig)
    if numerical_columns:
        if st.sidebar.checkbox('Correlation Matrix'):
            # Correlation heatmap for numerical columns
            numerical_data = df_train[numerical_columns]
            correlation_matrix = numerical_data.corr()

            fig, ax = plt.subplots(figsize=(8, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5, fmt=".2f")
            ax.set_title('Correlation Heatmap for Numerical Columns')
            st.pyplot(fig)
# Function to show the Key Performance Indicators section
def show_kpis(df_train):
    st.title("Key Performance Indicators")

    # Calculate overall KPIs
    avg_tenure = df_train['tenure'].mean()
    avg_monthly_charges = df_train['MonthlyCharges'].mean()
    avg_total_charges = df_train['TotalCharges'].mean()
    total_monthly_charges = df_train['MonthlyCharges'].sum()
    total_total_charges = df_train['TotalCharges'].sum()

    # Calculate churn-specific KPIs
    churned_df = df_train[df_train['Churn'] == 'Yes']
    non_churned_df = df_train[df_train['Churn'] == 'No']

    avg_churned_tenure = churned_df['tenure'].mean()
    avg_non_churned_tenure = non_churned_df['tenure'].mean()

    avg_churned_monthly_charges = churned_df['MonthlyCharges'].mean()
    avg_non_churned_monthly_charges = non_churned_df['MonthlyCharges'].mean()

    avg_churned_total_charges = churned_df['TotalCharges'].mean()
    avg_non_churned_total_charges = non_churned_df['TotalCharges'].mean()

    # Display KPIs
    
    st.markdown(f"### Average Tenure {avg_tenure:.2f} years")
    st.markdown(f"### Average Monthly Charges: ${avg_monthly_charges:.2f}")
    st.markdown(f"### Average Total Charges: ${avg_total_charges:.2f}")
    st.markdown(f"### Total Monthly Charges: ${total_monthly_charges:.2f}")
    st.markdown(f"### Total Total Charges: ${total_total_charges:.2f}")

    st.markdown(f"### Churned Average Tenure: {avg_churned_tenure:.2f} years")
    st.markdown(f"### Non-Churned Average Tenure: {avg_non_churned_tenure:.2f} years")

    st.markdown(f"###  Churned Average Monthly Charges: ${avg_churned_monthly_charges:.2f}")
    st.markdown(f"### Non-Churned Average Monthly Charges: ${avg_non_churned_monthly_charges:.2f}")

    st.markdown(f"### Churned Average Total Charges: ${avg_churned_total_charges:.2f}")
    st.markdown(f"### Non-Churned Average Total Charges: ${avg_non_churned_total_charges:.2f}")

# Initializing connection and loading data
conn = initialize_connection()
df_1st = select_all_features()
df_2nd = load_csv_data('./Dataset/LP2_Telco-churn-second-2000.csv')
df_train = pd.concat([df_1st, df_2nd], ignore_index=True)
df_train['SeniorCitizen'] = df_train['SeniorCitizen'].replace({0: 'No', 1: 'Yes'})
boolean_columns = ['Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                    'TechSupport', 'StreamingTV', 'StreamingMovies', 'PaperlessBilling', 'Churn']
df_train[boolean_columns] = df_train[boolean_columns].replace({False: 'No', True: 'Yes'})
df_train['MultipleLines'] = df_train['MultipleLines'].replace('No phone service', 'No')
df_train['TotalCharges'] = pd.to_numeric(df_train['TotalCharges'], errors='coerce')
No_internet_service_columns = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
df_train[No_internet_service_columns] = df_train[No_internet_service_columns].replace('No internet service', 'No')

# Sidebar Navigation
sidebar_selection = st.sidebar.radio("Select Section", ["About Dashboard", "Explore", "Key Performance Indicators"])

# Display the selected section
if sidebar_selection == "About Dashboard":
    show_about_dashboard()
elif sidebar_selection == "Explore":
    show_explore(df_train)
else:
    show_kpis(df_train)
    