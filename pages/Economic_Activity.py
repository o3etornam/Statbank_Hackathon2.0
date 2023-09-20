import streamlit as st
from utility import query_builder, convert_df, data_filter, query_df
import pandas as pd
import plotly.express as px
import features, warehouse

st.title('Visualize any Economic Activity Data of your Choice')

query_semi_path = 'Economic Activity/'

st.header('Build API Query')

selected_cat = warehouse.warehouse['Economic Activity']

dataset = query_builder(features= features, age = features.age_group_1,
                        warehouse=selected_cat, query_semi_path=query_semi_path)

st.header('Filter Data for Visualization')
w_variable = dataset.columns[0]

filtered_df, location, education, gender, age_group = data_filter(dataset=dataset, 
                                                     w_variable=w_variable,
                                                       title= '')

st.header('Chat With The Data Powered by OpenAI')
prompt = st.text_input('What would you like to know')

query_df(dataset, prompt)

csv = convert_df(dataset)

st.subheader('Download Dataset as CSV')
st.download_button(
    'Download data as CSV',
    data = csv,
    file_name= f'{w_variable}.csv'
)