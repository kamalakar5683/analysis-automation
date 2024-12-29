import streamlit as st  
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from io import StringIO

# Cache for file loading to avoid re-loading on every rerun
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            # Load CSV and immediately convert it to JSON for optimization
            df = pd.read_csv(file)
            json_data = df.to_json(orient='records')  # Convert DataFrame to JSON
            df = pd.read_json(StringIO(json_data))    # Reload DataFrame from JSON
        elif file.name.endswith('.json'):
            df = pd.read_json(file)
        else:
            st.error("Unsupported file format. Please upload a CSV or JSON file.")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Handling Missing Values and Keeping Track of Removed Rows
@st.cache_data
def handle_missing_values(df):
    removed_rows = df[df.isnull().any(axis=1)]
    df_cleaned = df.dropna()
    return df_cleaned, removed_rows

# Removing Outliers and Keeping Track of Removed Rows
@st.cache_data
def remove_outliers(df):
    num_columns = df.select_dtypes(include=[np.number]).columns
    removed_outliers = pd.DataFrame()
    for col in num_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        removed = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        removed_outliers = pd.concat([removed_outliers, removed], ignore_index=True)
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df, removed_outliers

# Univariate Analysis with Plotly Enhancements
def univariate_analysis(df):
    st.subheader("Univariate Analysis")
    cat_columns = df.select_dtypes(include=['object']).columns
    for col in cat_columns:
        with st.expander(f"Distribution of {col}"):
            value_counts = df[col].value_counts().reset_index()
            value_counts.columns = [col, 'count']
            st.write(value_counts)
            fig = px.bar(value_counts, x=col, y='count', title=f'Distribution of {col}', color='count', color_continuous_scale='Viridis')
            st.plotly_chart(fig)

    num_columns = df.select_dtypes(include=[np.number]).columns
    for col in num_columns:
        with st.expander(f"Distribution of {col}"):
            st.write(df[col].describe())
            fig1 = px.histogram(df, x=col, nbins=20, title=f'Distribution of {col}', color_discrete_sequence=['#636EFA'])
            fig2 = px.box(df, y=col, title=f'Box Plot of {col}', color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig1)
            st.plotly_chart(fig2)

# Bivariate Analysis with Plotly Enhancements
def bivariate_analysis(df):
    st.subheader("Bivariate Analysis")
    num_columns = df.select_dtypes(include=[np.number]).columns
    if len(num_columns) > 1:
        correlation_matrix = df[num_columns].corr()
        st.write("Correlation Matrix:")
        st.write(correlation_matrix)

        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='Viridis',
            colorbar=dict(title="Correlation Coefficient")
        ))
        fig.update_layout(title='Correlation Heatmap')
        st.plotly_chart(fig)

    for col1 in num_columns:
        for col2 in num_columns:
            if col1 != col2:
                with st.expander(f"{col1} vs {col2}"):
                    fig = px.scatter(df, x=col1, y=col2, title=f'{col1} vs {col2}', color=df[col1], color_continuous_scale='Viridis')
                    st.plotly_chart(fig)

# Main Streamlit App
def main():
    st.title("Interactive EDA with Streamlit")
    st.write("Upload a dataset (CSV or JSON) to begin.")

    file = st.file_uploader("Upload your dataset (CSV or JSON):", type=['csv', 'json'])
    if file:
        df = load_data(file)
        if df is not None:
            st.subheader("Dataset Overview")
            st.write("Full Raw Dataset:")
            st.dataframe(df)

            st.write(f"**Original Dataset Dimensions:** {df.shape[0]} rows, {df.shape[1]} columns")

            # Handle Missing Values
            st.subheader("Handling Missing Values")
            df_cleaned, removed_missing = handle_missing_values(df)

            # Remove Outliers
            st.subheader("Removing Outliers")
            df_cleaned, removed_outliers = remove_outliers(df_cleaned)

            # Display Removed Rows (Missing Values & Outliers)
            if st.button("Show Removed Rows"):
                with st.expander("Removed Rows due to Missing Values"):
                    if removed_missing.empty:
                        st.write("No missing values were removed.")
                    else:
                        st.dataframe(removed_missing)

                with st.expander("Removed Rows due to Outliers"):
                    if removed_outliers.empty:
                        st.write("No outliers were removed.")
                    else:
                        st.dataframe(removed_outliers)

            st.subheader("Cleaned Dataset")
            st.dataframe(df_cleaned)
            st.write(f"**Cleaned Dataset Dimensions:** {df_cleaned.shape[0]} rows, {df_cleaned.shape[1]} columns")

            # Perform EDA on cleaned data with improved visualizations
            univariate_analysis(df_cleaned)
            bivariate_analysis(df_cleaned)

if __name__ == "__main__":
    main()
