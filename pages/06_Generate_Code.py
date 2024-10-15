import streamlit as st

st.title("Step 5: Generate Python/SQL Code")

if "transformation_steps" in st.session_state and st.session_state.transformation_steps:
    st.write("### Generated Python Code:")
    python_code = "\n".join(st.session_state.transformation_steps)
    st.code(python_code, language='python')

    # SQL Code could be generated similarly based on the transformation steps
    st.write("### Generated SQL Code (if applicable):")
    st.code("-- SQL equivalent could go here", language='sql')

    st.download_button('Download Python Code', python_code, file_name="transformations.py")

else:
    st.warning("No transformations applied yet.")
