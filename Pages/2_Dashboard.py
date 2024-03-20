import streamlit as st
import pandas as pd
import yaml
import matplotlib.pyplot as plt
import seaborn as sns

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
st.set_page_config(
    page_title='View Data',
    page_icon='',
    layout='wide'
)

# Function to load data
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
        
        # Function to show the Key Performance Indicators section
    def show_kpis(df_train):
        st.markdown("### Key Performance Indicators")
        st.subheader("Customer Demographics")
        st.write(f"Total Customers: {df_train.shape[0]}")
        st.write(f"Total Churned Customers: {df_train['Churn'].value_counts()[1]}")
        st.write(f"Total Non-Churned Customers: {df_train['Churn'].value_counts()[0]}")
        st.write(f"Churn Rate: {df_train['Churn'].value_counts()[1] / df_train.shape[0] * 100:.2f}%")
        st.write(f"Number of Senior Citizens: {len(df_train[df_train['SeniorCitizen'] == 'Yes'])}")
    
        # calculate overall KPIs
        avg_tenure = df_train['Tenure'].mean()
        avg_monthly_charges = df_train['MonthlyCharges'].mean()
        avg_total_charges = df_train['TotalCharges'].mean()
        total_monthly_charges = df_train['MonthlyCharges'].sum()
        total_total_charges = df_train['TotalCharges'].sum()
        
        # Function to show the Explore section
    def show_explore(df_train):
        st.markdown("### Exploratory Data Analysis ")
        st.sidebar.subheader("Filter among the following Options")

        numerical_columns = ['Tenure', 'MonthlyCharges', 'TotalCharges']
        categorical_columns = ['Gender', 'SeniorCitizen', 'PhoneService', 'StreamingMovies',
                                'Contract', 'PaperlessBilling', 'PaymentMethod', 'Churn']

        for column in categorical_columns:
            if st.sidebar.checkbox(f'{column} Distribution'):
                column_counts = df_train[column].value_counts()
                if len(column_counts) <= 2:
                    # Bar chart for few unique values
                    fig, ax = plt.subplots()
                    ax.bar(column_counts.index, column_counts, color=['#66c2a5', '#fc8d62'])
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

        for column in numerical_columns:
            if st.sidebar.checkbox(f'{column} Distribution'):
                    # Histogram for numerical values
                num_bins = st.slider(f'Select number of bins for {column}', min_value=5, max_value=50, value=20)
                fig, ax = plt.subplots()
                ax.hist(df_train[column], bins=num_bins, color='#8da0cb')
                ax.set_title(f'Distribution of {column}')
                ax.set_xlabel(column)
                ax.set_ylabel('Count')
                st.pyplot(fig)

            if st.sidebar.checkbox(f'{column} vs Churn'):
                fig, ax = plt.subplots()
                sns.histplot(data=df_train, x=column, hue='Churn', multiple='stack', bins=num_bins, kde=True,
                            palette=['#66c2a5', '#fc8d62'])
                ax.set_title(f'{column} distribution by Churn')
                ax.set_xlabel(column)
                ax.set_ylabel('Count')
                st.pyplot(fig)

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
