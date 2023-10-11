import requests
import json
import streamlit as st
import pandas as pd
import features
import plotly.express as px
from pandasai import SmartDataframe
from pandasai.llm import OpenAI



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


def filter_and_plot(dataset,query):
    sex,age_grp,local,edu = [],[],[],[]
    for obj in query['query']:
        if obj['code'] == "Geographic_Area":
            location =  obj['selection']['values']

        if obj['code'] == "Age":
            age_grp = obj['selection']['values']
        if obj['code'] == "Education":
            edu = obj['selection']['values']
        if obj['code'] == "Sex":
            sex = obj['selection']['values']
        if obj['code'] == "Locality":
            local = obj['selection']['values']

    w_variable = query['query'][0]['code']

    count = dataset.columns[-1]

    filtered = st.multiselect(f'What {w_variable} will you like to visualize',dataset[w_variable].unique(), 
                              default=dataset[w_variable].unique())
    filtered_df = dataset[dataset[w_variable].isin(filtered)]

    location = st.multiselect('Which Region will you like to filter by', filtered_df['Geographic_Area'].unique(),
                              default=filtered_df['Geographic_Area'].unique()[:5])
    bar_fig = px.bar(filtered_df[filtered_df['Geographic_Area'].isin(location)],
                       x='Geographic_Area', y=count, 
                      color=w_variable, barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
    st.plotly_chart(bar_fig, use_container_width=True) 

    if edu:
        education = st.multiselect('Which Education level will you like to visualize', filtered_df['Education'].unique(),
                                    default = filtered_df['Education'].unique())
        edu_fig = px.bar(filtered_df[filtered_df['Education'].isin(education)],
                        x=w_variable, y=count, 
                        color='Education', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
        st.plotly_chart(edu_fig, use_container_width=True) 

    if sex:
        gender = st.multiselect('Which gender will you like to filter by', filtered_df['Sex'].unique(),
                                default = filtered_df['Sex'].unique())
        gender_fig = px.bar(filtered_df[filtered_df['Sex'].isin(gender)],
                        x=w_variable, y=count, 
                        color='Sex', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
        st.plotly_chart(gender_fig, use_container_width=True) 

    if age_grp:
        age_group = st.multiselect('Which Age group will you like to filter by', filtered_df['Age'].unique())
        age_fig = px.bar(filtered_df[filtered_df['Age'].isin(age_group)],
                    x=w_variable, y=count, 
                    color='Age', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
        st.plotly_chart(age_fig, use_container_width=True)

    if local:
        llc = st.multiselect('Which gender will you like to filter by', filtered_df['Locality'].unique(),
                                default = filtered_df['Locality'].unique())
        llc_fig = px.bar(filtered_df[filtered_df['Locality'].isin(llc)],
                        x=w_variable, y=count, 
                        color='Locality', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
        st.plotly_chart(llc_fig, use_container_width=True) 


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


def transform(df,w_variable):
    count = df.columns[-1]
    df[count] = df[count].astype(int)
    
    group_col = [w_variable,'Geographic_Area']
    series_list = []
    for col in ['Sex','Education','Age','Locality']:
        if col in df.columns:
            group_col.append(col)
   
    grp = df.groupby(group_col)
    for variable in df[w_variable].unique():
        temp = grp[count].sum().loc[variable]
        temp.name = f'{w_variable}_{variable}' 
        series_list.append(temp)

    return series_list