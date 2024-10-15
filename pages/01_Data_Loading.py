import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import requests

# Initialize transformation steps if not already done
if "transformation_steps" not in st.session_state:
    st.session_state.transformation_steps = []

# Initialize the dataframe session state
if "df" not in st.session_state:
    st.session_state.df = None


# Helper function to connect to MySQL and get tables
def get_mysql_tables(host, user, password, db):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        return tables
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


# Helper function to load data from a MySQL table
def load_mysql_data(host, user, password, db, table):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        query = f"SELECT * FROM {table}"
        df = pd.read_sql(query, connection)
        return df
    except Error as e:
        st.error(f"Error loading data from MySQL: {e}")
        return None
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()


# Streamlit app starts here
st.title("Step 1: Upload Data")

# Choose data source type (CSV, JSON, MySQL, API)
data_source = st.radio(
    "Select data source type",
    ('CSV', 'JSON', 'MySQL', 'API')  # Added API option
)

# Data loading based on the user's choice
if data_source == 'CSV':
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

    if uploaded_file is not None:
        # Select the separator
        separator = st.selectbox("Select the separator for the CSV file", [',', ';', '\t', '|', 'Other'])

        # If 'Other' is selected, provide an input field for the user to specify a custom separator
        if separator == 'Other':
            separator = st.text_input("Enter your custom separator:", value=",")

        # Load CSV with the specified separator
        try:
            st.session_state.df = pd.read_csv(uploaded_file, sep=separator)
            st.session_state.transformation_steps.append(f"pd.read_csv('{uploaded_file.name}', sep='{separator}')")
            st.success("CSV file loaded successfully!")
            st.write("### Data Preview:")
            st.dataframe(st.session_state.df.head())
        except Exception as e:
            st.error(f"Error loading CSV file: {e}")

elif data_source == 'JSON':
    uploaded_file = st.file_uploader("Upload your JSON file", type=['json'])

    if uploaded_file is not None:
        # Load JSON
        try:
            st.session_state.df = pd.read_json(uploaded_file)
            st.session_state.transformation_steps.append(f"pd.read_json('{uploaded_file.name}')")
            st.success("JSON file loaded successfully!")
            st.write("### Data Preview:")
            st.dataframe(st.session_state.df.head())
        except ValueError as ve:
            st.error(f"Error loading JSON file: Invalid JSON format. {ve}")
        except Exception as e:
            st.error(f"Error loading JSON file: {e}")

elif data_source == 'MySQL':
    # User inputs for MySQL connection
    st.write("### MySQL Database Connection")
    mysql_host = st.text_input("Host", value="127.0.0.1")  # Use 127.0.0.1 instead of localhost
    mysql_user = st.text_input("Username", value="root")
    mysql_password = st.text_input("Password", type="password", value="")  # Assuming no password
    mysql_database = st.text_input("Database Name")

    if st.button("Get Tables"):
        # Get tables from MySQL
        tables = get_mysql_tables(mysql_host, mysql_user, mysql_password, mysql_database)
        if tables:
            selected_table = st.selectbox("Select a table to load", tables)
            if st.button("Load Data"):
                # Load data from the selected MySQL table
                df = load_mysql_data(mysql_host, mysql_user, mysql_password, mysql_database, selected_table)
                if df is not None:
                    st.session_state.df = df
                    st.session_state.transformation_steps.append(f"Loaded data from table '{selected_table}'")
                    st.success(f"Data loaded from MySQL table '{selected_table}' successfully!")
                    st.write("### Data Preview:")
                    st.dataframe(df.head())
        else:
            st.warning("No tables found in the specified database.")

elif data_source == 'API':
    # Input for API URL
    api_url = st.text_input("Enter API URL", "")

    if st.button("Fetch Data"):
        if api_url:
            try:
                # Fetch data from the API
                response = requests.get(api_url)
                response.raise_for_status()  # Raise an error for bad responses

                # Assuming the API returns JSON data
                data = response.json()

                # Convert data to DataFrame (adjust this depending on the structure of your data)
                if isinstance(data, dict):
                    df = pd.json_normalize(data)
                else:
                    df = pd.DataFrame(data)

                # Store the DataFrame in session state
                st.session_state.df = df
                st.session_state.transformation_steps.append(f"Fetched data from API '{api_url}'")

                # Show success message
                st.success("Data fetched successfully!")

                # Display the DataFrame
                st.write("### Data Preview:")
                st.dataframe(df.head())
                st.write(f"DataFrame Shape: {df.shape[0]} rows and {df.shape[1]} columns")

            except requests.exceptions.RequestException as req_err:
                st.error(f"Error fetching data from API: {req_err}")
            except ValueError as val_err:
                st.error(f"Error processing JSON data: {val_err}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter a valid API URL.")

# Only show preview if data is available
if st.session_state.df is None:
    st.warning("Please load data to proceed.")