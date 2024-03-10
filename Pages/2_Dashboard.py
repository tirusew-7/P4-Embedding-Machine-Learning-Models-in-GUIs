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

# st.title('Data from Database')
def show():
    st.title("Dashboard Page")
    # Your dashboard page content goes here
    st.write("This is the Dashboard Page content.")
    
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

conn = initialize_connection()

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

def select_all_features():
    query = "SELECT * FROM LP2_Telco_Churn_first_3000"
    df = query_database(query)
    return df

# Define the missing function for loading CSV data
@st.cache_data()
def load_csv_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")

# Specify the path to your CSV file
csv_file_path = './Dataset/LP2_Telco-churn-second-2000.csv'
df_2nd = load_csv_data(csv_file_path)

# Load data from the database
df_1st = select_all_features()

# Concatenate the two DataFrames
df_train = pd.concat([df_1st, df_2nd], ignore_index=True)
# Convert 'SeniorCitizen' to object in dataset
df_train['SeniorCitizen'] = df_train['SeniorCitizen'].replace({0: 'No', 1: 'Yes'})

# True to Yes, False to No, No Services to No
boolean_columns = ['Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                    'TechSupport', 'StreamingTV', 'StreamingMovies', 'PaperlessBilling', 'Churn']

# Replace False with 'No' and True with 'Yes' in the specified boolean columns
df_train[boolean_columns] = df_train[boolean_columns].replace({False: 'No', True: 'Yes'})

# Replace 'No phone service' with 'No' in the 'MultipleLines' column
df_train['MultipleLines'] = df_train['MultipleLines'].replace('No phone service', 'No')
df_train['TotalCharges'] = pd.to_numeric(df_train['TotalCharges'], errors='coerce')

# Replace 'No internet service' with 'No' in specified columns
No_internet_service_columns = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
df_train[No_internet_service_columns] = df_train[No_internet_service_columns].replace('No internet service', 'No')

if __name__ == "__main__":
    st.markdown('### Type of Visualisation(Univariate, Bivariate, or Multivariate)')
    visualization_type = st.selectbox("Select Visualization Type", ["Univariate Visualization", "Bivariate Visualization", "Multivariate Visualization"])
    # Display sub-visualizations based on the selected type
    if visualization_type == "Univariate Visualization":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('### Univariate Visualization')
            selected_visuals = st.selectbox("Select Visualization",
                                            options=['Demographic Distribution', 'Service Features Distribution',
                                                    'Cost Features Distribution (Categorical)', 'Numerical Features Distribution', 'Target Variable [Churn]'],
                                            key='selected_features')

        if selected_visuals == "Demographic Distribution":
            categorical_vars = ['gender', 'SeniorCitizen', 'Partner', 'Dependents']
            rows = 2
            cols = 2
            fig, axes = plt.subplots(rows, cols, figsize=(10, 8))  # Set a figure size for better visibility
            axes = axes.flatten()
            bar_colors = ['purple', 'blue', 'brown', 'red']
            for i, var in enumerate(categorical_vars):
                value_counts = (df_train[var].value_counts(normalize=True) * 100).round(1)
                bars = value_counts.plot(kind='bar', ax=axes[i], color=bar_colors)
                axes[i].set_title(var, fontweight='bold', color='blue')
                axes[i].set_ylabel('Percentage', fontweight='bold', color='purple')
                axes[i].set_xlabel('')
                axes[i].set_xticks([0, 1])  # Set x-axis ticks
                axes[i].set_xticklabels(['No', 'Yes'])  # Set x-axis labels
                for idx, value in enumerate(value_counts):
                    axes[i].text(idx, value + 0.5, f'{value}%', ha='center', fontweight='bold', color=bar_colors[idx])
                axes[i].tick_params(axis='x', rotation=0)  # Rotate x-axis labels if needed
                for tick, label in zip(axes[i].get_xticks(), axes[i].get_xticklabels()):
                    label.set_color(bar_colors[tick])
                    label.set_fontweight('bold')
            plt.tight_layout()
            st.pyplot(fig)

        elif selected_visuals == "Service Features Distribution":
            categorical_vars = ['PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
            rows = 3
            cols = 3
            fig, axes = plt.subplots(rows, cols, figsize=(15, 10))  # Set a figure size for better visibility
            axes = axes.flatten()
            bar_colors = ['purple', 'blue', 'brown', 'red']

            for i, var in enumerate(categorical_vars):
                value_counts = (df_train[var].value_counts(normalize=True) * 100).round(1)

                # Add print statements to check values
                print(f"Variable: {var}")
                print(f"Value Counts: {value_counts}")

                # Set x-axis ticks and labels dynamically based on unique values
                x_ticks = range(len(value_counts))
                x_labels = value_counts.index.tolist()

                bars = value_counts.plot(kind='bar', ax=axes[i], color=bar_colors)
                axes[i].set_title(var, fontweight='bold', color='blue')
                axes[i].set_ylabel('Percentage', fontweight='bold', color='purple')
                axes[i].set_xlabel('')
                axes[i].set_xticks(x_ticks)
                axes[i].set_xticklabels(x_labels)

                for idx, value in enumerate(value_counts):
                    axes[i].text(idx, value + 0.5, f'{value}%', ha='center', fontweight='bold', color=bar_colors[idx])

                axes[i].tick_params(axis='x', rotation=20)

                for tick, label in zip(axes[i].get_xticks(), axes[i].get_xticklabels()):
                    label.set_color(bar_colors[tick])
                    label.set_fontweight('bold')

            plt.tight_layout()
            st.pyplot(fig)

        elif selected_visuals == "Cost Features Distribution (Categorical)":
            categorical_vars = ['Contract', 'PaperlessBilling', 'PaymentMethod']
            rows = 1
            cols = 3
            fig, axes = plt.subplots(rows, cols, figsize=(15, 5))
            axes = axes.flatten()
            bar_colors = ['purple', 'blue', 'brown', 'red']

            for i, var in enumerate(categorical_vars):
                value_counts = (df_train[var].value_counts(normalize=True) * 100).round(1)

                # Add print statements to check values
                print(f"Variable: {var}")
                print(f"Value Counts: {value_counts}")

                x_ticks = range(len(value_counts))
                x_labels = value_counts.index.tolist()

                bars = value_counts.plot(kind='bar', ax=axes[i], color=bar_colors)
                axes[i].set_title(var, fontweight='bold', color='blue')
                axes[i].set_ylabel('Percentage', fontweight='bold', color='purple')
                axes[i].set_xlabel('')
                axes[i].set_xticks(x_ticks)
                axes[i].set_xticklabels(x_labels)

                for idx, value in enumerate(value_counts):
                    axes[i].text(idx, value + 0.5, f'{value}%', ha='center', fontweight='bold', color=bar_colors[idx])

                axes[i].tick_params(axis='x', rotation=20)

                for tick, label in zip(axes[i].get_xticks(), axes[i].get_xticklabels()):
                    label.set_color(bar_colors[tick])
                    label.set_fontweight('bold')
            plt.tight_layout()
            st.pyplot(fig)

        elif selected_visuals == 'Numerical Features Distribution':
            numerical_columns = df_train.select_dtypes(include=['int64', 'float64']).columns
            colors = ['purple', 'blue', 'darkblue']
            fig, axes = plt.subplots(1, len(numerical_columns), figsize=(12, 3), sharey=True)

            for i, (column, color) in enumerate(zip(numerical_columns, colors)):
                df_train[column].hist(ax=axes[i], grid=False, color=color)
                axes[i].set_title(column)
                axes[i].set_xlabel(column)  # Add x-axis label for better clarity

            plt.tight_layout()  # Adjust layout for better readability
            st.pyplot(fig)  # Display the plot using st.pyplot

        elif selected_visuals == 'Target Variable [Churn]':
            var = 'Churn'
            value_counts = df_train[var].value_counts(normalize=True) * 100
            fig, ax = plt.subplots(figsize=(7, 5))
            bar_colors = ['purple', 'blue']
            bars = value_counts.plot(kind='bar', color=bar_colors, ax=ax)
            ax.set_title(f'{var} Distribution', fontweight='bold', color='blue')
            ax.set_ylabel('Percentage', fontweight='bold', color='purple')
            ax.set_xlabel('')
            ax.set_xticks([0, 1])  # Set x-axis ticks
            ax.set_xticklabels(['No', 'Yes'])  # Set x-axis labels
            for idx, value in enumerate(value_counts):
                ax.text(idx, value + 0.5, f'{value:.1f}%', ha='center', fontweight='bold', color=bar_colors[idx])     
            ax.tick_params(axis='x', rotation=0)  # Rotate x-axis labels if needed
            for tick, label in zip(ax.get_xticks(), ax.get_xticklabels()):
                label.set_color(bar_colors[tick])
                label.set_fontweight('bold')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            pass

    elif visualization_type == "Bivariate Visualization":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('### Bivariate Visualization')
            bivariate_visuals = st.selectbox("Select Visualization",
                                            options=['Churn Vs Numeric Features', 
                                            'Churn Vs Categorical Features I', 
                                            'Churn Vs Categorical Features II', 'Churn vs Tenure'] ,
                                            key='selected_features')

        if bivariate_visuals == "Churn Vs Numeric Features":
            fig, axes = plt.subplots(1, 3, figsize=(12, 3))
            for i, column in enumerate(['TotalCharges', 'tenure', 'MonthlyCharges']):
                sns.kdeplot(df_train[df_train['Churn'] == 'Yes'][column], label=f'Churn', shade=True, ax=axes[i])
                sns.kdeplot(df_train[df_train['Churn'] == 'No'][column], label=f'No-Churn', shade=True, ax=axes[i])
                axes[i].set_title(f'Distribution of {column} by Churn', color='blue', fontweight='bold', fontsize=10)
                axes[i].set_xlabel(column, color='purple', fontweight='bold', fontsize=10)
                axes[i].set_ylabel('Density', color='purple', fontweight='bold', fontsize=10)
                axes[i].legend()
            plt.tight_layout()
            # Display the Matplotlib figure using st.pyplot
            st.pyplot(fig)

        elif bivariate_visuals == "Churn Vs Categorical Features I":
            categorical_vars = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService',
                                'OnlineSecurity']
            # Calculate the number of rows and columns needed
            num_rows = math.ceil(len(categorical_vars) / 4)
            num_cols = 4
            # Create subplots using Streamlit
            fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 12))  # Create subplots
            axes = axes.flatten()
            # Loop through categorical variables
            for i, var in enumerate(categorical_vars):
                sns.countplot(x=var, hue='Churn', data=df_train, palette=['blue', 'purple'], ax=axes[i])  # Create count plot
                axes[i].set_title(f'Churn Counts by {var}', color='blue', fontweight='bold', fontsize=9)  # Set title and labels
                axes[i].set_xlabel(var)  # Annotate each bar with the percentage
                total = len(df_train[var])
                for p in axes[i].patches:
                    percentage = '{:.1f}%'.format(100 * p.get_height() / total)
                    axes[i].annotate(percentage, (p.get_x() + p.get_width() / 2., p.get_height() + 0.3),
                                    ha='center', va='bottom', color=p.get_facecolor(), fontweight='bold')
            # Set a common y-axis label for the leftmost plots
            axes[0].set_ylabel('Count')
            # Modify the legend to match the colors of the bars
            handles, labels = axes[-1].get_legend_handles_labels()
            # Display the Matplotlib figure using st.pyplot
            st.pyplot(fig)

        elif bivariate_visuals == "Churn Vs Categorical Features II":
            categoric_vars = ['OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 
            'StreamingMovies','Contract', 'PaperlessBilling', 'PaymentMethod']
            # Calculate the number of rows and columns needed
            num_rows = math.ceil(len(categoric_vars) / 4)
            num_cols = 4
            # Create subplots using Streamlit
            fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 12))  # Create subplots
            axes = axes.flatten()
            # Loop through categorical variables
            for i, var in enumerate(categoric_vars):
                sns.countplot(x=var, hue='Churn', data=df_train, palette=['blue', 'purple'], ax=axes[i])  # Create count plot
                axes[i].set_title(f'Churn Counts by {var}', color='blue', fontweight='bold', fontsize=9)  # Set title and labels
                axes[i].set_xlabel(var)  # Annotate each bar with the percentage
                total = len(df_train[var])
                for p in axes[i].patches:
                    percentage = '{:.1f}%'.format(100 * p.get_height() / total)
                    axes[i].annotate(percentage, (p.get_x() + p.get_width() / 2., p.get_height() + 0.3),
                                    ha='center', va='bottom', color=p.get_facecolor(), fontweight='bold')
            # Set a common y-axis label for the leftmost plots
            axes[0].set_ylabel('Count')
            # Modify the legend to match the colors of the bars
            handles, labels = axes[-1].get_legend_handles_labels()
            # Display the Matplotlib figure using st.pyplot
            st.pyplot(fig)

        elif bivariate_visuals == 'Churn vs Tenure':
            churned_data = df_train[df_train['Churn'] == 'Yes']
            # Group by tenure and count churned customers
            tenure_churn_counts = churned_data.groupby('tenure').size().reset_index(name='count_churned')
            # Plotting the chart
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(tenure_churn_counts['tenure'], tenure_churn_counts['count_churned'], marker='o')
            ax.set(xlabel='Tenure', ylabel='Number of Churned Customers', title='Trend of Churn vs Tenure')

            # Display the plot using st.pyplot
            st.pyplot(fig)

        with col2:
            pass
    elif visualization_type == "Multivariate Visualization":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('### Multivariate Visualization')
            multivariate_visuals = st.selectbox("Select Visualization",
                                                options=['Numerical Pairplot', 'Correlation Matrix'],
                                                key='selected_features')

        if multivariate_visuals == "Numerical Pairplot":
            # Create pair plot with the cleaned dataset
            pair_plot = sns.pairplot(df_train[['tenure', 'MonthlyCharges', 'TotalCharges']])
            # Display the plot using st.pyplot
            st.pyplot(pair_plot.fig)
        elif multivariate_visuals == "Correlation Matrix":
            # Multivariate Analysis: Heatmap for the correlation matrix of numeric variables
            correlation_matrix = df_train[['tenure', 'MonthlyCharges', 'TotalCharges']].corr()
            # Create a figure and axis explicitly
            fig, ax = plt.subplots()
            # Plot the heatmap on the specified axis
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
            # Set title
            ax.set_title('Correlation Matrix Heatmap')
            # Display the plot using st.pyplot with the figure explicitly passed
            st.pyplot(fig)

        with col2:
            pass