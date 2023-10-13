import streamlit as st
from utility import convert_df, url, load_query, api_reader, transform, ananse
import pandas as pd
import features
from warehouse import warehouse, categories
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.title(':red[Merge and Analyze Data Across The Various Categories of PHC 2021 Data]')

merge_list = st.multiselect('Which category of PHC 2021 data will you like to merge from', categories)
with st.form(key='form2'):
    st.header('Merge Datasets')
    
    datasets = {}
    sub_cats = []
    transformed_list = []
    for cat in merge_list:
        for key in warehouse[cat].keys():
            sub_cats.append(key)

    selected_sub_cat = st.multiselect('Which datasets will you like to merge and analyze', sub_cats)
    level = st.selectbox('What level of anaysis will you be doing?', ['Regional','Disctrict'])

    submit_button  = st.form_submit_button('Merge Datasets')
for cat in merge_list:
    for key in selected_sub_cat:
        if key in warehouse[cat].keys():
            query_semi_path = f'{cat}/'
            url = url + warehouse[cat][key]['extension']
            query = load_query(path = query_semi_path + warehouse[cat][key]['query_path'])

            for obj in query['query']:
                if obj['code'] == "Geographic_Area":
                    if level == 'Regional':
                        obj['selection']['values'] = features.regions
                    else:
                        obj['selection']['values'] = features.districts

        

            data, columns = api_reader(url= url,query=query)
            dataset = pd.DataFrame(data,columns=columns)
            w_variable = dataset.columns[0]
            count = dataset.columns[-1]
            dataset[count] = dataset[count].astype(float)
            datasets[key] = dataset

           
            transformed_list += (transform(dataset,w_variable = w_variable))
            

            url = 'https://statsbank.statsghana.gov.gh:443/api/v1/en/PHC 2021 StatsBank/'

if transformed_list:
    transformed_dfs = pd.concat(transformed_list, axis = 'columns')

    with st.expander('Click to view (merged) dataset'):
        st.dataframe(transformed_dfs)
        st.subheader('Download Dataset as CSV')
        csv = convert_df(transformed_dfs)
        st.download_button(
            'Download data as CSV',
            data = csv,
            file_name = 'merged.csv'
        )

    file = st.file_uploader('Upload a dataset to merge with data on statbank')
    if file:
        with st.expander('Click to view uploaded dataset'):
            st.dataframe(file)

    with st.expander('Click to view a profile report on merged datasets'):
        selected_cols = st.multiselect('Select the columns you will like to ptofile',transformed_dfs.columns)
        if selected_cols:
            pr = ProfileReport(transformed_dfs[selected_cols], title = 'Profiling Report')
            st.subheader('Profiling report')
            st_profile_report(pr)


    
    st.subheader('Chat with merged datasets powered by OpenAI')
    ananse(transformed_dfs)
