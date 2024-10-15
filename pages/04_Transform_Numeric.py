import streamlit as st

st.title("Step 4: Numeric Data Transformations")

if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

    if numeric_columns:
        st.write(f"### Numeric Columns: {numeric_columns}")

        fill_na_columns = st.multiselect('Select columns to fill missing values with mean', numeric_columns)

        if st.button('Apply Fill NA'):
            df[fill_na_columns] = df[fill_na_columns].fillna(df[fill_na_columns].mean())
            st.session_state.transformation_steps.append(
                f"df[{fill_na_columns}] = df[{fill_na_columns}].fillna(df[{fill_na_columns}].mean())"
            )
            st.success("Missing values filled with mean.")

        st.write("### Transformed Data Preview:")
        st.dataframe(df.head())
    else:
        st.write("No numeric columns to transform.")
else:
    st.warning("Please upload a CSV file first.")
