import streamlit as st

st.title("Step 3: String Data Transformations")

if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df
    string_columns = df.select_dtypes(include=['object']).columns.tolist()

    if string_columns:
        st.write(f"### String Columns: {string_columns}")

        clean_columns = st.multiselect('Select columns to clean whitespaces', string_columns)

        if st.button('Apply Cleaning'):
            df[clean_columns] = df[clean_columns].apply(lambda col: col.str.strip())
            st.session_state.transformation_steps.append(
                f"df[{clean_columns}] = df[{clean_columns}].apply(lambda col: col.str.strip())"
            )
            st.success("Whitespace cleaned in selected columns.")

        st.write("### Transformed Data Preview:")
        st.dataframe(df.head())
    else:
        st.write("No string columns to transform.")
else:
    st.warning("Please upload a CSV file first.")
