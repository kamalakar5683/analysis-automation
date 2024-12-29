Interactive EDA with Streamlit
This is an interactive Exploratory Data Analysis (EDA) tool built with Streamlit that allows you to upload datasets (CSV or JSON) and perform various data analysis tasks such as handling missing values, removing outliers, and performing univariate and bivariate analysis. The tool uses Plotly for creating interactive and visually appealing plots.

Features
Data Upload: Upload your dataset in CSV or JSON format.
Data Cleaning:
Handle missing values by removing rows with any null values.
Detect and remove outliers using the Interquartile Range (IQR) method.
Univariate Analysis:
Displays the distribution of categorical features using bar charts.
Visualizes the distribution of numerical features using histograms and box plots.
Bivariate Analysis:
Displays the correlation matrix between numerical features.
Creates scatter plots to explore relationships between pairs of numerical features.
Interactive Visualizations: Uses Plotly to render interactive charts and graphs.
Requirements
To run this project, you will need the following Python packages:

streamlit
pandas
numpy
plotly
scipy
You can install the required packages using the following command:

Copy code
pip install streamlit pandas numpy plotly scipy
How to Use
Clone this repository or download the script.
Run the Streamlit app using the following command:
arduino
Copy code
streamlit run app.py
Open your browser to the Streamlit interface (usually at http://localhost:8501).
Upload a CSV or JSON file to begin.
The app will display the dataset's overview, handle missing values, remove outliers, and provide insightful visualizations for both univariate and bivariate analysis.
Code Overview
Functions:
load_data(file): Loads the dataset from a CSV or JSON file and converts it into a DataFrame.
handle_missing_values(df): Handles missing data by removing rows containing null values.
remove_outliers(df): Removes outliers using the IQR method and returns the cleaned dataset.
univariate_analysis(df): Performs univariate analysis on both categorical and numerical columns and visualizes their distributions.
bivariate_analysis(df): Performs bivariate analysis and creates correlation matrices and scatter plots between numerical columns.
App Flow:
The app begins by prompting the user to upload a dataset.
After the dataset is loaded, the app shows the raw data, along with the dataset dimensions (number of rows and columns).
The app cleans the data by handling missing values and outliers.
Interactive visualizations of the data distribution and correlations are displayed.
The cleaned dataset is shown along with options to inspect the rows removed due to missing values or outliers.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
Streamlit for providing an easy and interactive interface.
Plotly for creating beautiful and interactive plots.
Pandas and NumPy for data manipulation and analysis.
