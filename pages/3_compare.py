import streamlit as st
from utility import geo_df

st.title(':red[Compare Data from the PHC 2021 to Other PHC Data]')

st.write(geo_df[['District', 'Region', 'geometry']].head())
