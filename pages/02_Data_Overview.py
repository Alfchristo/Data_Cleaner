import streamlit as st

st.title("Step 2: Data Overview")

if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df

    st.write("### Data Info:")
    st.write(df.info())  # Prints info to the console
    st.write("### Data Description (Numeric Columns):")
    st.write(df.describe())
else:
    st.warning("Please upload a CSV file first.")
