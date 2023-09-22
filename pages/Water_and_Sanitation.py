import streamlit as st
from utility import query_builder, convert_df, filter_and_plot
import pandas as pd
import plotly.express as px
import features

st.title('Visualize any Water and Sanitation Datasets of your Choice')

st.header('Build API Query')

query_semi_path = 'ICT/'

warehouse = {'Ownership of Laptops':{'extension': 'ICT/ownict_table_4.px','query_path':'Own_laptop.json'},
           'Ownership of Functional Mobile':{'extension':'ICT/ownmobile_table.px','query_path':'Own_functional_mobile.json'},
           }

dataset = query_builder(features= features, age = features.age_group_2,
                        warehouse=warehouse, query_semi_path=query_semi_path)

st.subheader('Dataset Extracted with API Query')
st.dataframe(dataset)

st.header('Filter Data for Visualization')
w_variable = dataset.columns[0]
count = dataset.columns[-1]

filter_and_plot(dataset = dataset,w_variable = w_variable,count = count ,title = '')


csv = convert_df(dataset)
st.download_button(
    'Download data as CSV',
    data = csv,
    file_name= f'{w_variable}.csv'
)