# Home Page 
import streamlit as st
import re

# Define username and password requirements
USERNAME = 'Tirusew'
PASSWORD = 'Chat@5555'
MIN_PASSWORD_LENGTH = 8

def is_valid_password(password):
    # Check if the password meets the specified requirements
    return len(password) >= MIN_PASSWORD_LENGTH and any(char.isdigit() for char in password) and any(char.isascii() and not char.isalnum() for char in password)

def main():
    st.title('Customer Churn Prediction')

    # Add login section
    username_input = st.text_input('Username')
    password_input = st.text_input('Password', type='password')

    if st.button('Login'):
        if username_input == USERNAME and is_valid_password(password_input):
            st.success('Logged in as {}'.format(username_input))
            # Display the main app content here
            show_main_app_content()
        else:
            st.error('Invalid username or password. Please try again.')

def show_main_app_content():
    # Content for the home page
    st.header('Welcome to the Customer Churn Prediction App')

    st.subheader('Data')
    st.write("""
    Explore and analyze the dataset used for customer churn prediction. 
    View details such as the number of records, features, and statistical summaries.
    """)

    st.subheader('Dashboard')
    st.write("""
    Visualize insights and trends related to customer churn through interactive charts and graphs.
    Dive into the data to gain a better understanding of the factors influencing churn.
    """)

    st.subheader('Predict')
    st.write("""
    Make predictions for individual customers based on their characteristics. 
    Input the required information, and the app will provide a churn prediction.
    """)

    st.subheader('History')
    st.write("""
    Access a record of predictions made and view the historical data of customer churn predictions.
    Keep track of past predictions and analyze the accuracy of the model over time.
    """)

if __name__ == '__main__':
    main()
