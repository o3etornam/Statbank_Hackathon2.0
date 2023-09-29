import streamlit as st
from utility import query_builder, convert_df, filter_and_plot
import pandas as pd
import plotly.express as px
import features, warehouse

st.title('Visualize any Data Across Various Categories of PHC 2021 Data')
selected_cat = st.selectbox('Which PHC 2021 data will you like to visualize', warehouse.categories)
query_semi_path = f'{selected_cat}/'

st.header('Build API Query')

category = warehouse.warehouse[selected_cat]

dataset = query_builder(features= features,
                        warehouse=category, query_semi_path=query_semi_path)

st.subheader('Dataset Extracted with API Query')
with st.expander('Click to view a dataset extracted dataframe the statsbank'):
    st.dataframe(dataset)

st.header('Filter Data for Visualization')
w_variable = dataset.columns[0]
count = dataset.columns[-1]

filter_and_plot(dataset = dataset,w_variable = w_variable,count = count ,title = '')

csv = convert_df(dataset)

st.subheader('Download Dataset as CSV')
st.download_button(
    'Download data as CSV',
    data = csv,
    file_name= f'{w_variable}.csv'
)

prompt = st.text