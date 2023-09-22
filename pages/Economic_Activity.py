import streamlit as st
from utility import query_builder, convert_df, filter_and_plot, query_df
import pandas as pd
import plotly.express as px
import features, warehouse

st.title('Visualize any Economic Activity Data of your Choice')

query_semi_path = 'Economic Activity/'

st.header('Build API Query')

selected_cat = warehouse.warehouse['Economic Activity']

dataset = query_builder(features= features, age = features.age_group_1,
                        warehouse=selected_cat, query_semi_path=query_semi_path)

st.subheader('Dataset Extracted with API Query')
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