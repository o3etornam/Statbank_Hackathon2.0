import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title='VisualChat', page_icon=':bar_chart:', initial_sidebar_state='auto')

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

data_animation = load_lottieurl("https://lottie.host/354b9800-749a-4f12-885e-03df61fb100c/FRlU5MUfxm.json")
chat_animation = load_lottieurl("https://lottie.host/7d239120-2e4a-460f-916b-e7d83012e53a/eyOh5ACb5R.json")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Welcome to VisualChat</h1>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("<h3 style=''>A platform where one can perform visual analysis of data from PHC Statsbank 2021 and chat with the bot to get insights.</h3>", unsafe_allow_html=True)


st.markdown("<h2 style='text-align: center;'>What we offer</h2>", unsafe_allow_html=True)

st.write("---")

with st.container():
    left_col, right_col = st.columns(2)
    with left_col:
        st.header(":blue[Data Visualisation at its best]")
        st.write("##")
        st.write(
            """
               It provides an intuitive way to analyze and unlock insights from PHC Statsbank 2021, empowering you with powerful data visualization tools. Our web app offers a seamless experience for exploring and understanding complex data sets. With a wide array of chart types and customization options, you can effortlessly create stunning visual representations of your data. Whether you're a data enthusiast, researcher, or business professional, our platform simplifies the process of transforming raw data into meaningful insights. Discover trends, patterns, and correlations with ease, and leverage the power of data to make informed decisions. Visualize, interact, and gain valuable insights into your data like never before.
            """)
    with right_col:
        st_lottie(data_animation, height=350, key="data_animation") 
        
with st.container():
    left_col, right_col = st.columns(2)
    with left_col:
        st.header("Interactive Data Chatbot")
        st.write("##")
        st.write(
            """
               DataBot is your virtual data assistant, ready to answer questions, provide insights, and guide you through the data exploration process. Whether you're a data enthusiast, researcher, or business professional, our platform simplifies the process of transforming raw data into meaningful insights. Discover trends, patterns, and correlations with ease, and leverage the power of data to make informed decisions. Visualize, interact, and gain valuable insights into your data like never before, all while having a conversation with DataBot to enhance your data exploration experience.
            """)
    with right_col:
        st.write("##")
        st_lottie(chat_animation, height=300, key="chat_animation")        