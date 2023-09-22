import requests
import json
import streamlit as st
import pandas as pd
import features
import plotly.express as px
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from dotenv import load_dotenv
import os

session = requests.Session()
url = 'https://statsbank.statsghana.gov.gh:443/api/v1/en/PHC 2021 StatsBank/'

load_dotenv()
api_key = st.secrets["OPENAI_API_KEY"]

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

    education = st.multiselect('Which Education level will you like to filter by', features.education, max_selections= 5,
                                       default=["Never attended","Primary","Secondary","Tertiary - Bachelor's Degree"], key = '4')
    for obj in query['query']:
        if obj['code'] == "Education":
            obj['selection']['values'] = education


    data, columns = api_reader(url= url,query=query)
    dataset = pd.DataFrame(data,columns=columns)

    return dataset

def filter_and_plot(dataset,w_variable,count,title):
    filtered = st.multiselect(f'What {w_variable} will you like to visualize',dataset[w_variable].unique(), 
                              default=dataset[w_variable].unique())
    filtered_df = dataset[dataset[w_variable].isin(filtered)]
    location = st.multiselect('Which Region will you like to filter by', filtered_df['Geographic_Area'].unique(),
                              default=filtered_df['Geographic_Area'].unique()[:5])
    bar_fig = px.bar(filtered_df[filtered_df['Geographic_Area'].isin(location)],
                       x='Geographic_Area', y=count, 
                      color=w_variable, barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
    st.plotly_chart(bar_fig, use_container_width=True) 

    education = st.multiselect('Which Education level will you like to visualize', filtered_df['Education'].unique(),
                                default = filtered_df['Education'].unique())
    edu_fig = px.bar(filtered_df[filtered_df['Education'].isin(education)],
                       x=w_variable, y=count, 
                      color='Education', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
    st.plotly_chart(edu_fig, use_container_width=True) 

    gender = st.multiselect('Which gender will you like to filter by', filtered_df['Sex'].unique(),
                            default = filtered_df['Sex'].unique())
    gender_fig = px.bar(filtered_df[filtered_df['Sex'].isin(gender)],
                       x=w_variable, y=count, 
                      color='Sex', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
    st.plotly_chart(gender_fig, use_container_width=True) 

    if len(filtered_df['Age'].unique()) > 1:
        age_group = st.multiselect('Which Age group will you like to filter by', filtered_df['Age'].unique())
        age_fig = px.bar(filtered_df[filtered_df['Age'].isin(age_group)],
                       x=w_variable, y=count, 
                      color='Age', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
        st.plotly_chart(age_fig, use_container_width=True)

llm = OpenAI(api_token=api_key)

@st.cache_resource
def query_df(df,prompt,llm = llm):
    df = SmartDataframe(df, config={"llm": llm})
    if prompt:
        return st.write(df.chat(prompt))