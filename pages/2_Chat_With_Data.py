import streamlit as st
from utility import query_builder, convert_df, url, load_query, api_reader
import pandas as pd
import features, warehouse
#from pandasai import SmartDataframe
#from pandasai.llm import OpenAI

from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

from langchain.llms import OpenAI





api_key = st.secrets["OPENAI_API_KEY"]
#llm = OpenAI(api_token=api_key)

st.title('Chat with any Data Across Various Categories of PHC 2021 Data powered by OpenAI')
merge_list = st.multiselect('Which PHC 2021 data will you like to visualize', warehouse.categories)

datasets = {}
sub_cats = []
for cat in merge_list:
    for key in warehouse.warehouse[cat].keys():
        sub_cats.append(key)

selected_sub_cat = st.multiselect('what to talkk', sub_cats)
level = st.selectbox('What level of visualization do want?', ['Regional','Disctrict'])
education = st.multiselect('Which Education level will you like to filter by', features.education, max_selections= 5,
                                       default=["Never attended","Primary","Secondary","Tertiary - Bachelor's Degree"])

for cat in merge_list:
    for key in selected_sub_cat:
        if key in warehouse.warehouse[cat].keys():
            query_semi_path = f'{cat}/'
            url = url + warehouse.warehouse[cat][key]['extension']
            query = load_query(path = query_semi_path + warehouse.warehouse[cat][key]['query_path'])

            if level == 'Regional':
                for obj in query['query']:
                    if obj['code'] == "Geographic_Area":
                        obj['selection']['values'] = features.regions
            else:
                for obj in query['query']:
                    if obj['code'] == "Geographic_Area":
                        obj['selection']['values'] = features.districts

            for obj in query['query']:
                if obj['code'] == "Age":
                    obj['selection']['values'] = [warehouse.warehouse[cat][key]['age'][0]] 

            for obj in query['query']:
                if obj['code'] == "Education": 
                    obj['selection']['values'] = education

            data, columns = api_reader(url= url,query=query)
            dataset = pd.DataFrame(data,columns=columns)
            w_variable = dataset.columns[0]
            dataset = dataset.set_index([w_variable,'Geographic_Area','Sex','Education','Age'])
            datasets[key] = dataset

            url = 'https://statsbank.statsghana.gov.gh:443/api/v1/en/PHC 2021 StatsBank/'

if datasets.keys():
    view = st.selectbox('Which dataset will you like to view', datasets.keys())
    with st.expander('Click to view dataset'):
        st.dataframe(datasets[view])

    st.subheader('Chat with Data')
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model= 'gpt-3.5-turbo'),
        datasets[view],
        verbose=True
        )

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "What will you like to know?"}]

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "What will you like to know?"}]

    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

    # Function for generating LLaMA2 response
    @st.cache_resource
    def query_df(prompt,agent = agent):
        if prompt:
            return agent.run(prompt)

    # User-provided prompt
    if prompt := st.chat_input(disabled=not api_key):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = query_df(prompt)
                placeholder = st.empty()
                full_response = ''
                if response:
                    for item in response:
                        full_response += item
                        placeholder.markdown(full_response)
                        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})