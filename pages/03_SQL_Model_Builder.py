# pages/sql_model.py

import streamlit as st
import pandas as pd


def recommend_sql_type(column, dtype, max_length=None):
    """ Recommends SQL type based on Pandas dtype and optional max length for strings """
    if pd.api.types.is_integer_dtype(dtype):
        return "INT"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    elif pd.api.types.is_object_dtype(dtype):
        if max_length and max_length <= 255:
            return f"VARCHAR({max_length})"
        else:
            return "TEXT"
    else:
        return "TEXT"


# Streamlit page for SQL model recommendation

st.title("Step 3: SQL Model Recommendation")

    # Check if data is available in session
if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df

    st.write("### Data Overview")
    st.dataframe(df.head())

    # SQL table name input
    table_name = st.text_input("Enter Table Name:", value="your_table_name")

    # Begin SQL Create Table statement
    create_statement = f"CREATE TABLE {table_name} (\n"

    # Analyze columns and recommend SQL types
    for column in df.columns:
        dtype = df[column].dtype
        max_length = None

        # For string columns, calculate max length
        if pd.api.types.is_object_dtype(df[column]):
            max_length = df[column].astype(str).map(len).max()

        # Recommend SQL type
        sql_type = recommend_sql_type(column, dtype, max_length)
        create_statement += f"  {column} {sql_type},\n"

    # Close SQL statement
    create_statement = create_statement.rstrip(",\n") + "\n);"

    # Display the generated SQL Create Table statement
    st.text_area("SQL Create Table Statement:", value=create_statement, height=200)

    st.success("SQL Table Schema generated based on your dataset.")

else:
    st.warning("Please upload or load data first.")


# Render the SQL model page

