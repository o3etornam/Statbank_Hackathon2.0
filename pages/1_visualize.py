import streamlit as st
from utility import convert_df, filter_and_plot, url, load_query, api_reader, ananse, transform
import pandas as pd
import plotly.express as px
from warehouse import warehouse
import features

st.title(':red[Visualize any Data Across Various Categories of PHC 2021 Data]')
selected_cat = st.selectbox('Which PHC 2021 data will you like to visualize', warehouse)
query_semi_path = f'{selected_cat}/'

st.header('Build API Query')

category = warehouse[selected_cat]

selected = st.selectbox('Select the data you want to visualize',category.keys(), key='1')
level = st.selectbox('What level of visualization do want?', ['National','Regional','Disctrict'], key = '2')

url += category[selected]['extension']
query = load_query(path = query_semi_path + category[selected]['query_path'])
age = category[selected]['age']

if level == 'National':
    for obj in query['query']:
        if obj['code'] == "Geographic_Area":
            obj['selection']['values'] = ['Ghana']

elif level == 'Regional':
    for obj in query['query']:
        if obj['code'] == "Geographic_Area":
            obj['selection']['values'] = features.regions
else:
    for obj in query['query']:
        if obj['code'] == "Geographic_Area":
            obj['selection']['values'] = features.districts
    
age_group = st.multiselect('Which Age group will you like to filter by', age, max_selections= 5)
for obj in query['query']:
        if obj['code'] == "Age":
                obj['selection']['values'] = age_group

education = st.multiselect('Which education level will you like to filter by', features.education, max_selections= 5,key = '4')
for obj in query['query']:
    if obj['code'] == "Education":
        obj['selection']['values'] = education

sex = st.multiselect('Which gender will you like to filter by', ['Male','Female'])
for obj in query['query']:
    if obj['code'] == "Sex":
        obj['selection']['values'] = sex

data, columns = api_reader(url= url,query=query)
dataset = pd.DataFrame(data,columns=columns)

w_variable = dataset.columns[0]
count = dataset.columns[-1]

dataset[count] = dataset[count].astype(int)


transformed = pd.concat(transform(dataset,w_variable = w_variable), axis='columns')

st.subheader('Dataset Extracted with API Query')
with st.expander('Click to view a dataset extracted dataframe the statsbank'):
    st.dataframe(transformed)
    st.subheader('Download Dataset as CSV')
    csv = convert_df(transformed)
    st.download_button(
        'Download data as CSV',
        data = csv,
        file_name = f'{selected}.csv'
    )

st.subheader('Filter Data for Visualization')

filter_and_plot(dataset = dataset,w_variable = w_variable,count = count,
                age_grp=age_group,
                edu = education,
                sex = sex)

st.subheader('Chat with data powered by OpenAI')
ananse(transformed)