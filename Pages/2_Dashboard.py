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
df_train = pd.read_csv('Dataset\Cleaned_data.csv')
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
            config['credentials']['usernames'][new_username] = {'email': '', 'logged_in': False, 'name': new_username, 'password': new_password}
            save_config()
            st.sidebar.success("Account created successfully. You can now log in.")
    
    st.warning("You need to log in or create an account to access the data.")
else:
    # Authenticate user login
    username = st.session_state['name']
    password = st.text_input("Password", type="password")

    @st.cache
    def load_csv_data(df_train):
        try:
            df = pd.read_excel(df_train)
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
        st.write(f"Total Monthly Charges: ${df_train['MonthlyCharges'].sum():,.2f}")
        st.write(f"Total Tenure: {df_train['Tenure'].sum()} months")
             
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

        # Sidebar Navigation
    sidebar_selection = st.sidebar.radio("Select Section", ["About Dashboard", "Explore", "Key Performance Indicators"])
        
        # Display the selected section
    if sidebar_selection == "About Dashboard":
        show_about_dashboard()
    elif sidebar_selection == "Explore":
        show_explore(df_train)
    else:
        show_kpis(df_train)
