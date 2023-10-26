import streamlit as st
from utility import convert_df, url, load_query, api_reader, ananse, transform, extract_pop_data, geo_json
import pandas as pd
import plotly.express as px
from warehouse import warehouse, individual_cat
import features


st.header(':blue[Visualize any Data Across Various Categories of PHC 2021 Data]')

selected_cat = st.selectbox('Which PHC 2021 data will you like to visualize', warehouse.keys())
st.session_state['selected_cat'] = selected_cat
with st.form(key='form1'):
    query_semi_path = f'{selected_cat}/'

    st.header(':blue[Build API Query]')

    category = warehouse[st.session_state['selected_cat']]

    selected = st.selectbox('Select the data you want to visualize (*required)',category.keys(), key='1')
    st.session_state['selected'] = selected
    level = st.selectbox('What level of visualization do want? ', ['District','Region','Country'], key = '2')

    url += f"{st.session_state['selected_cat']}/{category[st.session_state['selected']]['extension']}"
    query = load_query(path = query_semi_path + category[st.session_state['selected']]['query_path'])

    if 'age' in category[selected].keys():
        age = category[selected]['age']


    for obj in query['query']:
        if obj['code'] == "Geographic_Area":
            if level == 'Country':
                obj['selection']['values'] = ['Ghana']
            elif level == 'Region':
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
count = dataset.columns[-1]
dataset = dataset.rename(columns = {'Geographic_Area':level})
w_variable = dataset.columns[0]
dataset[count] = dataset[count].astype(float)


if w_variable not in [level, 'Sex', 'Education','Age', 'Locality']:
    transformed = pd.concat(transform(dataset,level = level,w_variable = w_variable), axis='columns')
    df = transformed
else:
    df = dataset

st.subheader(':blue[Dataset Extracted with API Query]')
with st.expander('Click to view a dataset extracted dataframe the statsbank'):
    st.dataframe(df)
    file, file_format = convert_df(df)
    st.subheader(f'Download Dataset as {file_format}')
    st.download_button(
        f'Download data as {file_format}',
        data = file,
        file_name = f'{w_variable}.{file_format}'
    )

st.subheader(':blue[Filter Data for Visualization]')

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

if w_variable in [level,'Sex','Age','Locality','Education']:
    filtered_df = dataset
else:
    filtered = st.multiselect(f'What {w_variable} will you like to visualize',dataset[w_variable].unique(), 
                            default=dataset[w_variable].unique())
    filtered_df = dataset[dataset[w_variable].isin(filtered)]
location = st.multiselect('Which Region will you like to filter by', filtered_df[level].unique(),
                            default=filtered_df[level].unique()[:5])
bar_fig = px.bar(filtered_df[filtered_df[level].isin(location)],
                    x=level, y=count, 
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
    
selected_variable = st.selectbox(f'What {w_variable} variable will you like analyze across {level}s in Ghana',df.columns)
adj = False
if selected_cat in individual_cat: 
    if selected not in ['Unemployment Rate','Population by Geographic Area']:
        pop_df = pd.read_csv(f'{level}.csv')
        pop_df = pop_df[[f'{level}','Population']].set_index(f'{level}')
        adj_df = pd.concat([df,pop_df], axis = 'columns')
        adj = True
  
df_name = df.reset_index()
ghana_fig = px.choropleth(df_name, geojson=geo_json, locations=level, color=selected_variable,
                           color_continuous_scale="Blues",
                           scope="africa",
                           featureidkey="properties.District",
                           labels={'Employed':'Number of employed'}
                          )
ghana_fig.update_geos(fitbounds="locations", visible=False)
ghana_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(ghana_fig, use_container_width=True)

if adj:
    with st.expander('Click to view the adjusted graph'):
        st.write(f'The adjusted graph scales data with respect to the {level.lower()} population')
        adj_df = adj_df.reset_index()
        adj_df[f'Adj.{selected_variable}'] = adj_df[selected_variable]/adj_df['Population'] * 100
        adj = ghana_fig = px.choropleth(adj_df, geojson=geo_json, locations=level, color=f'Adj.{selected_variable}',
                                color_continuous_scale="Blues",
                                scope="africa",
                                featureidkey="properties.District",
                                labels={'Employed':'Number of employed'}
                                )
        ghana_fig.update_geos(fitbounds="locations", visible=False)
        ghana_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(ghana_fig, use_container_width=True)


st.subheader(':blue[Chat with Nyansapo powered by OpenAI]')
ananse(df.reset_index())

