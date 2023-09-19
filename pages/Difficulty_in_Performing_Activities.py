import streamlit as st
from utility import query_builder, convert_df, data_filter
import pandas as pd
import plotly.express as px
import features

st.title('Visualize any Difficulty in Performing Activities Datasets of your Choice')

st.header('Build API Query')

query_semi_path = 'ICT/'

warehouse = {'Ownership of Laptops':{'extension': 'ICT/ownict_table_4.px','query_path':'Own_laptop.json'},
           'Ownership of Functional Mobile':{'extension':'ICT/ownmobile_table.px','query_path':'Own_functional_mobile.json'},
           }

dataset = query_builder(features= features, age = features.age_group_2,
                        warehouse=warehouse, query_semi_path=query_semi_path)

st.header('Filter Data for Visualization')
w_variable = dataset.columns[0]

filtered_df, location, education, gender, age_group = data_filter(dataset=dataset, 
                                                     w_variable=w_variable,
                                                       title= '')

csv = convert_df(dataset)
st.download_button(
    'Download data as CSV',
    data = csv,
    file_name= f'{w_variable}.csv'
)