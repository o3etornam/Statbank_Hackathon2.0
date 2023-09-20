import streamlit as st
from utility import query_builder, convert_df, data_filter
import pandas as pd
import plotly.express as px
import features, warehouse

st.title('Merge and Compare Data Across Various Categories of PHC 2021 Data')
merge_list = st.sidebar.selectbox('Which PHC 2021 data will you like to visualize', warehouse.categories)