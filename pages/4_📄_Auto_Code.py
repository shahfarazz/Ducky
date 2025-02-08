import asyncio
import nest_asyncio
import streamlit as st
from aitools_autogen.utils import clear_working_dir
from aitools_autogen.blueprint_project8 import DataAnalysisScriptsGenerator
import helpers.sidebar

# Apply nest_asyncio to enable running asyncio tasks in Streamlit
nest_asyncio.apply()

st.set_page_config(page_title="Data Analysis Scripts Generator",
                   page_icon="📊", layout="wide")

helpers.sidebar.show()

if 'data_analysis_blueprint' not in st.session_state:
    st.session_state['data_analysis_blueprint'] = DataAnalysisScriptsGenerator()


async def run_analysis():
    data_description = st.session_state['data_description']
    await st.session_state['data_analysis_blueprint'].initiate_work(data_description)
    return st.session_state['data_analysis_blueprint'].files_summary

prefill_text = """The dataset consists of monthly sales data from a chain of electronics stores from January 2020 to December 2022. Each record in the dataset includes the following columns: 'Date', 'Store ID', 'Product ID', 'Units Sold', and 'Revenue'.

I need a Python script that:
1. Reads this data from a CSV file named 'monthly_sales.csv'.
2. Calculates the total revenue and total units sold for each product across all stores.
3. Computes the average monthly revenue per store.
4. Generates a line plot showing the trend of total revenue over time.

The script should handle any missing data by ignoring records with missing values and should include comments explaining each step of the process.
"""

data_description_input = st.text_area("Enter the description of your data and the analysis you need:",
                                      value=prefill_text)
if st.button("Generate Analysis Script"):
    st.session_state['data_description'] = data_description_input
    st.session_state['analysis_result'] = asyncio.run(run_analysis())
    st.experimental_rerun()

results_container = st.container()
with results_container:
    if 'analysis_result' in st.session_state:
        st.write(st.session_state['analysis_result'])
        st.snow()
