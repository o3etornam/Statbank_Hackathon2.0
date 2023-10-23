import streamlit as st
from utility import convert_df, url, load_query, api_reader, ananse, transform, extract_pop_data
import pandas as pd
import plotly.express as px
from warehouse import warehouse
import features

st.title(':red[Visualize any Data Across Various Categories of PHC 2021 Data]')
selected_cat = st.selectbox('Which PHC 2021 data will you like to visualize', warehouse)
with st.form(key='form1'):
    query_semi_path = f'{selected_cat}/'

    st.header('Build API Query')

    category = warehouse[selected_cat]

    selected = st.selectbox('Select the data you want to visualize (*required)',category.keys(), key='1')
    level = st.selectbox('What level of visualization do want? ', ['National','Regional','Disctrict'], key = '2')

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
    
    submit_button  = st.form_submit_button('Run Query')

if submit_button:
    submit_button = False

data, columns = api_reader(url= url,query=query)
dataset = pd.DataFrame(data,columns=columns)
w_variable = dataset.columns[0]
count = dataset.columns[-1]

dataset[count] = dataset[count].astype(float)

adj = True
if selected in ['Unemployment Rate','Population by Geographic Area']:
    adj = False
if adj:
    pop_dataset, merge_on = extract_pop_data(query)
    pop_dataset['Population'] = pop_dataset['Population'].astype(float)
    adj_df = pd.merge(dataset,pop_dataset, on= merge_on)
    adj_df['Adj. Population'] = (adj_df[count] / adj_df['Population']) * 100

    with st.expander('debugging on going. click to understand'):
         st.dataframe(adj_df)

if w_variable not in ['Geographic_Area', 'Sex', 'Education','Age', 'Locality']:
    transformed = pd.concat(transform(dataset,w_variable = w_variable), axis='columns')
    df = transformed
else:
    df = dataset
st.subheader('Dataset Extracted with API Query')
with st.expander('Click to view a dataset extracted dataframe the statsbank'):
    st.dataframe(df)
    file, file_format = convert_df(df)
    st.subheader(f'Download Dataset as {file_format}')
    st.download_button(
        f'Download data as {file_format}',
        data = file,
        file_name = f'merged.{file_format}'
    )

st.subheader('Filter Data for Visualization')

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

if w_variable in ['Geographic_Area','Sex','Age','Locality','Education']:
    filtered_df = dataset
    if adj:
        filtered_adj_df = adj_df
else:
    filtered = st.multiselect(f'What {w_variable} will you like to visualize',dataset[w_variable].unique(), 
                            default=dataset[w_variable].unique())
    filtered_df = dataset[dataset[w_variable].isin(filtered)]
    if adj:
        filtered_adj_df = adj_df[adj_df[w_variable].isin(filtered)] 

location = st.multiselect('Which Region will you like to filter by', filtered_df['Geographic_Area'].unique(),
                            default=filtered_df['Geographic_Area'].unique()[:5])
bar_fig = px.bar(filtered_df[filtered_df['Geographic_Area'].isin(location)],
                    x='Geographic_Area', y=count, 
                    color=w_variable, barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
st.plotly_chart(bar_fig, use_container_width=True)
if adj:
    adj_bar_fig = px.bar(filtered_adj_df[filtered_adj_df['Geographic_Area'].isin(location)],
                    x='Geographic_Area', y='Adj. Population', 
                    color=w_variable, barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
    with st.expander('Click to view the adjusted plot'):
        st.plotly_chart(adj_bar_fig, use_container_width=True)

if edu:
    education = st.multiselect('Which Education level will you like to visualize', filtered_df['Education'].unique(),
                    default = filtered_df['Education'].unique())
    edu_fig = px.bar(filtered_df[filtered_df['Education'].isin(education)],
        x=w_variable, y=count, 
        color='Education', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
    st.plotly_chart(edu_fig, use_container_width=True)
    if adj:
        adj_edu_fig = px.bar(filtered_adj_df[filtered_adj_df['Education'].isin(education)],
                        x=w_variable, y='Adj. Population', 
                        color='Education', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
        with st.expander('Click to view the adjusted plot'):
                st.plotly_chart(adj_edu_fig, use_container_width=True)

if sex:
    gender = st.multiselect('Which gender will you like to filter by', filtered_df['Sex'].unique(),
                            default = filtered_df['Sex'].unique())
    gender_fig = px.bar(filtered_df[filtered_df['Sex'].isin(gender)],
                        x=w_variable, y=count, 
                        color='Sex', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
    st.plotly_chart(gender_fig, use_container_width=True)
    if adj:
        adj_sex_fig = px.bar(filtered_adj_df[filtered_adj_df['Sex'].isin(gender)],
                        x=w_variable, y='Adj. Population', 
                        color='Sex', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
        with st.expander('Click to view the adjusted plot'):
                st.plotly_chart(adj_sex_fig, use_container_width=True)



if age_grp:
    age_group = st.multiselect('Which Age group will you like to filter by', filtered_df['Age'].unique())
    age_fig = px.bar(filtered_df[filtered_df['Age'].isin(age_group)],
                x=w_variable, y=count, 
                color='Age', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
    st.plotly_chart(age_fig, use_container_width=True)
    if adj:
        adj_age_fig = px.bar(filtered_adj_df[filtered_adj_df['Age'].isin(age_group)],
                        x=w_variable, y='Adj. Population', 
                        color='Age', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
        with st.expander('Click to view the adjusted plot'):
                st.plotly_chart(adj_age_fig, use_container_width=True)

if local:
    llc = st.multiselect('Which gender will you like to filter by', filtered_df['Locality'].unique(),
                                default = filtered_df['Locality'].unique())
    llc_fig = px.bar(filtered_df[filtered_df['Locality'].isin(llc)],
                        x=w_variable, y=count, 
                        color='Locality', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
    st.plotly_chart(llc_fig, use_container_width=True)
    if adj:
        adj_llc_fig = px.bar(filtered_adj_df[filtered_adj_df['Locality'].isin(llc)],
                        x=w_variable, y='Adj. Population', 
                        color='Locality', barmode='group', title=f'Grouped Bar Plot showing across regions in Ghana')
        with st.expander('Click to view the adjusted plot'):
                st.plotly_chart(adj_llc_fig, use_container_width=True)


st.subheader('Chat with data powered by OpenAI')
ananse(df)