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

def artists_on_the_map():

    title = "Location of listened Artists"
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"""<div class="big-title">{title}</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        sel_person = st.selectbox("Choose user", ["Maciek", "Ola"])

    continent_cords = {
        "Europe" : dict(lat=48, lon=24),
        "Asia" : dict(lat=35, lon=90),
        "Africa" : dict(lat=-8, lon=23),
        "North America" : dict(lat=31, lon=-97),
        "South America" : dict(lat=-34, lon=-58),
        "Australia/Oceania" : dict(lat=-24, lon=148)
    }

    with col2:
        sel_continent = st.selectbox("Chose continent", continent_cords.keys())

    if sel_person == "Ola":
        df = get_artist_loc(data_ola)
        df2 = count_counties(data_ola, sel_continent)
        color = colors_ola[3]
    else:
        df = get_artist_loc(data_maciek)
        df2 = count_counties(data_ola, sel_continent)
        color = colors_maciek[3]

    st.plotly_chart(plotly_scatter_map(df, mapbox_token, "lat", "lon", continent_cords[sel_continent], color),
                    use_container_width=True)

    col, = st.columns(1)

    with col:
        sel_num_of_countries = st.slider(
            "Select number of countries",
            min_value=1,
            max_value=df2.shape[0],
            value=df2.shape[0]//2)

    st.plotly_chart(plotly_bar_chart(df2, color, sel_num_of_countries))