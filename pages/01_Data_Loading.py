import streamlit as st
import pandas as pd

st.title("Step 1: Upload CSV File")

uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)
    st.session_state.transformation_steps = []  # Reset transformations when a new file is loaded
    st.success("File uploaded successfully!")
    st.write("### Data Preview:")
    st.dataframe(st.session_state.df.head())
else:
    st.warning("Please upload a CSV file to proceed.")
