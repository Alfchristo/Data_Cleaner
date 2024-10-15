import streamlit as st
import pandas as pd

st.title("Step 2: Data Overview")

# Check if DataFrame is in session state
if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df

    st.subheader("Data Overview")

    # Display the shape of the dataframe (rows, columns)
    st.write(f"**Shape of the DataFrame:** {df.shape[0]} rows, {df.shape[1]} columns")

    # Display column names and data types
    st.write("### Column Names and Data Types")
    column_info = pd.DataFrame({
        'Column Name': df.columns,
        'Data Type': df.dtypes
    })
    st.dataframe(column_info)

    # Display missing values per column
    st.write("### Missing Values per Column")
    missing_values = df.isnull().sum().reset_index()
    missing_values.columns = ['Column', 'Missing Values']
    missing_values['% Missing'] = (missing_values['Missing Values'] / len(df)) * 100
    st.dataframe(missing_values)

    # Filter out columns with unhashable types like dictionaries or lists
    hashable_columns = []
    unhashable_columns = []
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
            unhashable_columns.append(col)
        else:
            hashable_columns.append(col)

    # Display unique values per hashable column
    if hashable_columns:
        st.write("### Unique Values per Column (Hashable Columns Only)")
        unique_values = df[hashable_columns].nunique().reset_index()
        unique_values.columns = ['Column', 'Unique Values']
        st.dataframe(unique_values)
    else:
        st.warning("No hashable columns available for unique value calculation.")

    # Display a message for unhashable columns
    if unhashable_columns:
        st.warning(f"The following columns contain unhashable types (like lists or dictionaries) and are excluded from unique value calculation: {', '.join(unhashable_columns)}")

    # Data Description for Numeric Columns
    st.write("### Data Description (for Numeric Columns)")
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_columns) > 0:
        st.dataframe(df.describe())
    else:
        st.write("No numeric columns available for description.")

    # Allow user to select specific columns for more detailed description
    st.write("### Select Columns to Describe")
    columns_to_describe = st.multiselect(
        "Select columns for detailed description", df.columns
    )

    if columns_to_describe:
        st.write("### Detailed Description of Selected Columns")
        st.dataframe(df[columns_to_describe].describe())

else:
    st.warning("Please upload or load data first.")
