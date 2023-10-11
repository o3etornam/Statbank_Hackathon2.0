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

url += f"{selected_cat}/{category[selected]['extension']}"
query = load_query(path = query_semi_path + category[selected]['query_path'])

if 'age' in category[selected].keys():
    age = category[selected]['age']


for obj in query['query']:
    if obj['code'] == "Geographic_Area":
        if level == 'National':
            obj['selection']['values'] = ['Ghana']
        elif level == 'Regional':
            obj['selection']['values'] = features.regions
        else:
            obj['selection']['values'] = features.districts
    
    if obj['code'] == "Age":
        obj['selection']['values'] = st.multiselect('Which Age group will you like to filter by', age, max_selections= 5)

    if obj['code'] == "Education":
        obj['selection']['values'] = st.multiselect('Which education level will you like to filter by', features.education, max_selections= 5)

    if obj['code'] == "Sex":
        obj['selection']['values'] = st.multiselect('Which gender will you like to filter by', ['Male','Female'])

    if obj['code'] == "Locality":
        obj['selection']['values'] = st.multiselect('Which locality will you like to filter by', ['Rural','Urban'])
    


data, columns = api_reader(url= url,query=query)
dataset = pd.DataFrame(data,columns=columns)
w_variable = dataset.columns[0]
count = dataset.columns[-1]

dataset[count] = dataset[count].astype(float)

if w_variable not in ['Geographic_Area', 'Sex', 'Education','Age', 'Locality']:
    transformed = pd.concat(transform(dataset,w_variable = w_variable), axis='columns')
    df = transformed
else:
    df = dataset
st.subheader('Dataset Extracted with API Query')
with st.expander('Click to view a dataset extracted dataframe the statsbank'):
    st.dataframe(df)
    st.subheader('Download Dataset as CSV')
    csv = convert_df(df)
    st.download_button(
        'Download data as CSV',
        data = csv,
        file_name = f'{selected}.csv'
    )

st.subheader('Filter Data for Visualization')

filter_and_plot(dataset = dataset,query = query)

st.subheader('Chat with data powered by OpenAI')
ananse(transformed)