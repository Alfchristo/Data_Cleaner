import streamlit as st

# Main entry point
st.title("CSV Transformation App")
st.write("Welcome! Use the sidebar to navigate through the steps.")

# Optional: You can also provide a brief description here.
st.write("""
This app allows you to:
1. Load a CSV file.
2. View the data overview.
3. Apply transformations (cleaning, grouping, etc.).
4. Generate Python/SQL code to replicate the transformations.
""")

if "transformation_steps" not in st.session_state:
    st.session_state.transformation_steps = []
if "df" not in st.session_state:
    st.session_state.df = None
