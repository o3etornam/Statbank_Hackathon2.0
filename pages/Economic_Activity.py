import streamlit as st
from utility import query_builder, convert_df, data_filter, query_df
import pandas as pd
import plotly.express as px
import features, warehouse

st.title('Visualize any PHC 2021 Data of your Choice')

category = st.sidebar.selectbox('Which PHC 2021 data will you like to visualize', warehouse.categories)
query_semi_path = f'{category}/'

st.header('Build API Query')

selected_cat = warehouse.warehouse[category]

dataset = query_builder(features= features, age = features.age_group_1,
                        warehouse=selected_cat, query_semi_path=query_semi_path)

st.header('Filter Data for Visualization')
w_variable = dataset.columns[0]

filtered_df, location, education, gender, age_group = data_filter(dataset=dataset, 
                                                     w_variable=w_variable,
                                                       title= '')


query_df(dataset)

csv = convert_df(dataset)
st.download_button(
    'Download data as CSV',
    data = csv,
    file_name= f'{w_variable}.csv'
)