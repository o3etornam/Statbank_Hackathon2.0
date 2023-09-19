import requests
import json
import streamlit as st
import pandas as pd
import features
import pandasai
import openai

session = requests.Session()
url = 'https://statsbank.statsghana.gov.gh:443/api/v1/en/PHC 2021 StatsBank/'

@st.cache_data
def api_reader(url, query):
    response = session.post(url, json=query)
    response_json = json.loads(response.content.decode('utf-8-sig'))
    columns = [item['text'] for item in response_json['columns']]
    data = [item['key'] + item['values'] for item in response_json['data']]
    return data, columns

@st.cache_data
def convert_df(df):
    return df.to_csv()

@st.cache_data
def load_query(path, root = 'queries/'):
    full_path = root + path
    with open(full_path) as json_file:
        query = json.load(json_file)
    
    return query

def query_builder(warehouse,features,age,query_semi_path, url = url):
    selected = st.selectbox('Select the data you want to visualize',warehouse.keys(), key='1')
    level = st.selectbox('What level of visualization do want?', ['National','Regional','Disctrict'], key = '2')

    url = url + warehouse[selected]['extension']
    query = load_query(path = query_semi_path + warehouse[selected]['query_path'])

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
    
    age_group = st.multiselect('Which Age group will you like to filter by', age, max_selections= 5,
                           default=[age[0]], key = '3')
    for obj in query['query']:
        if obj['code'] == "Age":
                obj['selection']['values'] = age_group

    education = age_group = st.multiselect('Which Education level will you like to filter by', features.education, max_selections= 5,
                                       default=["Never attended","Primary","Secondary","Tertiary - Bachelor's Degree"], key = '4')
    for obj in query['query']:
        if obj['code'] == "Education":
            obj['selection']['values'] = education


    data, columns = api_reader(url= url,query=query)
    dataset = pd.DataFrame(data,columns=columns)

    return dataset

def data_filter(dataset,w_variable, title):
    filtered = st.multiselect(f'What {title} will you like to visualize',dataset[w_variable].unique())

    filtered_df = dataset[dataset[w_variable].isin(filtered)]

    location = st.multiselect('Which Region will you like to filter by', filtered_df['Geographic_Area'].unique())
    education = age_group = st.multiselect('Which Education level will you like to filter by', filtered_df['Education'].unique()) 
    gender = st.multiselect('Which gender will you like to filter by', filtered_df['Sex'].unique())
    age_group = st.multiselect('Which Age group will you like to filter by', filtered_df['Age'].unique())

    return filtered_df,location, education, gender, age_group 
