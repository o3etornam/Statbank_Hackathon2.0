import streamlit as st
from utility import convert_df, url, load_query, api_reader, transform, ananse
import pandas as pd
import features
from warehouse import warehouse, categories, individual_cat, housing_cat
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import numpy as np
import matplotlib.pyplot as plt
from plotly.figure_factory import create_dendrogram
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, normalize


st.header(':blue[Merge and Analyze Data Across The Various Categories of PHC 2021 Data]')
allow_merge = st.selectbox('What kind of data collection source will you like to merge on', ['Individuals', 'Households'])
if allow_merge == 'Individuals':
    data_source = individual_cat
else:
    data_source = housing_cat
merge_list = st.multiselect('Which of the thematic areas of PHC 2021 data will you like to merge from', data_source)
with st.form(key='form2'):
    st.subheader(':blue[Merge Datasets]')
    
    datasets = {}
    sub_cats = []
    transformed_list = []
    for cat in merge_list:
        for key in warehouse[cat].keys():
            sub_cats.append(key)

    selected_sub_cat = st.multiselect('Which of the categories will you like to merge and analyze (*required)', sub_cats)
    level = 'Disctrict'

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
            dataset = dataset.rename(columns = {'Geographic_Area':level})
            datasets[key] = dataset
            

           
            transformed_list += (transform(dataset,level = level,w_variable = w_variable,multiple=True))
            

            url = 'https://statsbank.statsghana.gov.gh:443/api/v1/en/PHC 2021 StatsBank/'

if transformed_list:
    transformed_dfs = pd.concat(transformed_list, axis = 'columns')
    merged = False

    with st.expander('Click to view (merged) dataset'):
        st.dataframe(transformed_dfs)
        file, file_format = convert_df(transformed_dfs)
        st.subheader(f':blue[Download Dataset as {file_format}]')
        st.download_button(
            f'Download data as {file_format}',
            data = file,
            file_name = f'merged.{file_format}'
        )
    st.subheader(':blue[Upload a dataset to merge with data on statbank]')
    file = st.file_uploader('')
    if file:
        uploaded_df = pd.read_csv(file)
        with st.expander('Click to view uploaded dataset'):
            st.dataframe(uploaded_df)

        st.warning(f'Datasets will be merged on {level} level. {level}s from the Statsbank are in title case')
        right_on = st.multiselect('Which column will you like to merge on',uploaded_df.columns,max_selections=1)
        merged_df = pd.merge(transformed_dfs,uploaded_df,left_on='Geographic_Area', right_on=right_on)

        with st.expander('Click to view merged datasets'):
            st.dataframe(merged_df)
        merged = True

    
    st.subheader(':blue[Profile merged datasets]')
    with st.expander('Click to view a profile report on merged datasets'):
        if merged:
            profile_df = merged_df
        else:
            profile_df = transformed_dfs
        selected_cols = st.multiselect('Select the columns you will like to ptofile',profile_df.columns)
        if selected_cols:
            pr = ProfileReport(profile_df[selected_cols], title = 'Profiling Report')
            st.subheader('Profiling report')
            st_profile_report(pr)

    st.subheader(':blue[Cluster Analysis]')
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(profile_df)
    X_normalized = normalize(X_scaled)
    cluster_df = pd.DataFrame(X_normalized, columns = profile_df.columns, index=profile_df.index)
    dendro = create_dendrogram(X_normalized)
    dendro['layout'].update({'title':'Dendrogram of merged dataset'})
    st.plotly_chart(dendro)
    

    n = st.slider('Select the number of clusters you want',2, 10, 2)
    cluster = AgglomerativeClustering(n_clusters=n)
    profile_df['cluster'] = cluster.fit_predict(cluster_df)
    st.dataframe(profile_df['cluster'])

    st.subheader(':blue[Chat with Nyansapo powered by OpenAI]')
    ananse(transformed_dfs)
