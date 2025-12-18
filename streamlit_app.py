import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import sys
import lyricsgenius
from wordcloud import WordCloud, STOPWORDS
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from streamlit_lottie import st_lottie
import json
import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import *
import spotipy
import pickle
from utils2 import *
from home import *
from shared import *

st.set_page_config(layout="wide")
st.write("<style>" + open(STYLE_PATH).read() + "</style>", unsafe_allow_html=True)

st.sidebar.title("choose data")
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Shared", "playlists on the map", "generate your own spotify wrapped", "Summary"],
        styles = {"nav-link-selected":{"background-color": "#202035"} }
    )

st.markdown('<div class="big-title">Spotify Dashboard Overview</div>', unsafe_allow_html=True)
st.caption("This app was created to analyse trends present in our music taste")

if selected == "Home":
    home()

if selected == "Shared":
    shared()
