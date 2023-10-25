import requests
import json
import streamlit as st
import pandas as pd
import features
import plotly.express as px
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from geojson_rewind import rewind
import geopandas as gpd
from urllib.request import urlopen



session = requests.Session()
url = 'https://statsbank.statsghana.gov.gh:443/api/v1/en/PHC 2021 StatsBank/'

@st.cache_data
def get_geo():
    with urlopen('https://raw.githubusercontent.com/Laurent-Smeets-GSS-Account/geojsons/main/geojsons_files/Drophole.geojson') as json_file:
        geojson = json.load(json_file)
    return rewind(geojson,rfc7946=False)

geo_json = get_geo()


@st.cache_data
def api_reader(url, query):
    response = session.post(url, json=query)
    response_json = json.loads(response.content.decode('utf-8-sig'))
    columns = [item['text'] for item in response_json['columns']]
    data = [item['key'] + item['values'] for item in response_json['data']]
    return data, columns


def convert_df(df):
    file_formats = {'csv':df.to_csv}
    selected_file_format = st.radio('What format will you like to save the dataset as',file_formats.keys())
    return file_formats[selected_file_format](), selected_file_format

@st.cache_data
def load_query(path, root = 'queries/'):
    full_path = root + path
    with open(full_path) as json_file:
        query = json.load(json_file)
    
    return query 


api_key = st.secrets["OPENAI_API_KEY"]
llm = OpenAI(api_token=api_key)

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "What will you like to know?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

def ananse(df):
    df = SmartDataframe(df, config={"llm": llm})

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "What will you like to know?"}]

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input(disabled=not api_key):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = df.chat(prompt)
                placeholder = st.empty()
                full_response = ''
                if response:
                    for item in response:
                        full_response += item
                        placeholder.markdown(full_response)
                        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


def transform(df,w_variable,level,multiple = False):
    count = df.columns[-1]
    
    if not w_variable in [level,'Sex','Age','Locality','Education']:
        group_col = [w_variable,level]
        series_list = []
        for col in ['Sex','Education','Age','Locality']:
            if col in df.columns:
                group_col.append(col)
   
        grp = df.groupby(group_col)
        for variable in df[w_variable].unique():
            temp = grp[count].sum().loc[variable]
            if multiple:
                temp.name = f'{w_variable}_{variable}' 
            else:
                temp.name = variable
            series_list.append(temp)

        return series_list
    temp = df.set_index(level)[count]
    return [temp]


@st.cache_data
def extract_pop_data(data_query, level):
    merge_key = level
    pop_url = 'https://statsbank.statsghana.gov.gh:443/api/v1/en/PHC 2021 StatsBank/Population/population_table.px'
    #pop_query = load_query('Population/population.json')
    if level == 'Region':
        geo_area = features.regions
    else:
        geo_area = features.districts
    pop_query = {
            "query": [
      {
        "code": "Hearing",
        "selection": {
          "filter": "item",
          "values": geo_area
        }
      }],
      "response": {
      "format": "json"
    }
      }
    st.write(pop_url)
    st.write(pop_query)

    pop_data, pop_columns = api_reader(url= pop_url,query=pop_query)
    return pd.DataFrame(pop_data,columns=pop_columns), merge_key
