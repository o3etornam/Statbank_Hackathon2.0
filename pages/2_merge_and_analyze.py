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
if submit_button:
    submit_button = False
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

           
            transformed_list += (transform(dataset,w_variable = w_variable,multiple=True))
            

            url = 'https://statsbank.statsghana.gov.gh:443/api/v1/en/PHC 2021 StatsBank/'

if transformed_list:
    transformed_dfs = pd.concat(transformed_list, axis = 'columns')

    with st.expander('Click to view (merged) dataset'):
        st.dataframe(transformed_dfs)
        file, file_format = convert_df(transformed_dfs)
        st.subheader(f'Download Dataset as {file_format}')
        st.download_button(
            f'Download data as {file_format}',
            data = file,
            file_name = f'merged.{file_format}'
        )

    file = st.file_uploader('Upload a dataset to merge with data on statbank')
    if file:
        uploaded_df = pd.read_csv(file)
        with st.expander('Click to view uploaded dataset'):
            st.dataframe(uploaded_df)

        right_on = st.selectbox('Which column will you like to merge on',uploaded_df.columns)
        merged_df = pd.merge(transformed_dfs,uploaded_df,left_on='Geographic_Area', right_on=right_on)

    with st.expander('Click to view a profile report on merged datasets'):
        selected_cols = st.multiselect('Select the columns you will like to ptofile',transformed_dfs.columns)
        if selected_cols:
            pr = ProfileReport(transformed_dfs[selected_cols], title = 'Profiling Report')
            st.subheader('Profiling report')
            st_profile_report(pr)


    
    st.subheader('Chat with merged datasets powered by OpenAI')
    ananse(transformed_dfs)
