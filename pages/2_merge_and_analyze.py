import streamlit as st
from utility import query_builder, convert_df, url, load_query, api_reader, transform, ananse
import pandas as pd
import features
from warehouse import warehouse, categories

st.title(':red[Ananse]')
merge_list = st.multiselect('Which PHC 2021 data will you like to visualize', categories)

datasets = {}
sub_cats = []
transformed_list = []
for cat in merge_list:
    for key in warehouse[cat].keys():
        sub_cats.append(key)

selected_sub_cat = st.multiselect('what to talkk', sub_cats)
level = st.selectbox('What level of visualization do want?', ['Regional','Disctrict'])
education = st.multiselect('Which Education level will you like to filter by', features.education, max_selections= 5)
sex = st.multiselect('Which gender level will you like to filter by', ['Male','Female'])

for cat in merge_list:
    for key in selected_sub_cat:
        if key in warehouse[cat].keys():
            query_semi_path = f'{cat}/'
            url = url + warehouse[cat][key]['extension']
            query = load_query(path = query_semi_path + warehouse[cat][key]['query_path'])

            if level == 'Regional':
                for obj in query['query']:
                    if obj['code'] == "Geographic_Area":
                        obj['selection']['values'] = features.regions
            else:
                for obj in query['query']:
                    if obj['code'] == "Geographic_Area":
                        obj['selection']['values'] = features.districts

            for obj in query['query']:
                if obj['code'] == "Sex":
                    obj['selection']['values'] = sex 

            for obj in query['query']:
                if obj['code'] == "Education": 
                    obj['selection']['values'] = education

            data, columns = api_reader(url= url,query=query)
            dataset = pd.DataFrame(data,columns=columns)
            w_variable = dataset.columns[0]
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

    ananse(transformed_dfs)
