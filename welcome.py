import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.set_page_config(page_title='Mligbalamo', page_icon=':bar_chart:', initial_sidebar_state='auto')

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# local_css("style/style.css")

data_animation = load_lottieurl("https://lottie.host/354b9800-749a-4f12-885e-03df61fb100c/FRlU5MUfxm.json")
chat_animation = load_lottieurl("https://lottie.host/7d239120-2e4a-460f-916b-e7d83012e53a/eyOh5ACb5R.json")

st.title("Mligbalamo.")

st.subheader("A platform provides an intuitive way to analyze and unlock insights from PHC Statsbank 2021, empowering you with powerful data visualization tools.")

st.divider()

st.subheader('Features :')
st.markdown('''
            * Use interactive plots to visualize PHC 2021 Data
            * Query datasets using natural language
            * Merge and analyze data across the multiple categories of the PHC 2021 Data
            * Compare PHC 2021 data to PHC data from different years
            ''')

st.divider()
st.markdown("<h2 style=''>What we offer :</h2>", unsafe_allow_html=True)

# st.write("---")


st.subheader("Data Visualisation at its best")
st.write("##")
st.write(
    """
        It provides an intuitive way to analyze and unlock insights from PHC Statsbank 2021, empowering you with powerful data visualization tools.
    """)

st_lottie(data_animation, height=450, key="data_animation") 

st.subheader("Interactive Data Chatbot")
st.write("##")
st.write(
"""
    Nyansapo is your virtual data assistant, ready to answer questions, provide insights, and guide you through the data exploration process.
""")
st.write("##")
st_lottie(chat_animation, height=400, key="chat_animation")        

# st.title(':red[Mligbalamo.]')
# st.header('WebApp built as an interractive wrapper on the PHC 2021 Data')
