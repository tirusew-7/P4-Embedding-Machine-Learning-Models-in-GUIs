import streamlit as st
import yaml

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

def create_account(username, password):
    if username in config['credentials']['usernames']:
        return False, "Username already exists. Please choose a different username."
    config['credentials']['usernames'][username] = {'email': '', 'logged_in': False, 'name': username, 'password': password}
    save_config()
    return True, "Account created successfully. You can now log in."

st.set_page_config(
    page_title="Vodafone Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"  
)

st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to bottom, #800000, #FFFFFF); /* Wine red to milk white gradient */
        width: 100vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)


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
        st.sidebar.success("Please enter your details below to create an account.")
        new_username = st.sidebar.text_input("New Username")
        new_password = st.sidebar.text_input("New Password", type="password")
        success, message = create_account(new_username, new_password)
        if not success:
            st.sidebar.error(message)
        else:
            st.sidebar.success(message)
    else:
        st.sidebar.title("Logout")
        if st.sidebar.button("Logout"):
            del st.session_state["name"]
            st.sidebar.success("You have been successfully logged out.")

        st.warning("You need to log in or create an account to access the data.")

# Function to display image and sidebar
def display_image_and_sidebar():
    st.image('images\Vodafone_Albania-Logo.wine.png', use_column_width=True)

    return st.sidebar.radio("Menu", ["About App"])

# Main application logic
menu_tab = display_image_and_sidebar()

if menu_tab == "About App":
    st.markdown("""
    Attrition Insight is a Machine Learning application that predicts the likelihood of an employee to leave the company based on various demographic and job-related factors.
 
    **Key Features**
    - View Data: Access proprietary data from IBM.
    - Dashboard: Explore interactive data visualizations for insights.
    - Real-time Prediction: Instantly see predictions for employee attrition.
    - History: See past predictions made.
 
    **User Benefits**
    - Data-driven Decisions.
    - Utilize powerful machine learning algorithms effortlessly.
                
    **How to run application**
    ```
    # activate virtual environment
    env/scripts/activate
    streamlit run 1_Home.py
    ```
 
    **Machine Learning Integration**
    - Model Selection: Choose between two advanced models for accurate predictions.
    - Seamless Integration: Integrate predictions into  workflow with a user-friendly interface.
    - Probability Estimates: Gain insights into the likelihood of predicted outcomes.
    """)
