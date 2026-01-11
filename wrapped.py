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

def wrapped():
    col1, col2= st.columns(2)
    with col1:
        sel_person = st.selectbox("Choose user", ["Maciek", "Ola"])
        if sel_person == "Ola":
            df = data_ola
            colors = colors_ola
            colors_light = colors_ola_light
        else:
            df = data_maciek
            colors = colors_maciek
            colors_light = colors_maciek_light

    df['ts_date'] = pd.to_datetime(df['ts_date'])
    data = df.copy()
    activity = data.groupby("ts_date")['ms_played'].sum()
    data = activity.reset_index() if isinstance(activity, pd.Series) else activity.copy()
    data['ts_date'] = pd.to_datetime(data['ts_date'])
    data['mins'] = (data['ms_played'] / 60000).round(0)
    available_years = sorted(data['ts_date'].dt.year.unique(), reverse=True)

    with col2:
        sel_year = st.selectbox("Year", available_years)

    met1, met2, met3, met4 = st.columns(4)

    with met1:
        diff = get_max_in_the_day(df, sel_year) - get_max_in_the_day(df, sel_year - 1)
        st.metric(
            label=f"Max hours in a day ({sel_year})",
            value=f"{get_max_in_the_day(df, sel_year):.1f}",
            delta=f"{diff:+,.1f} h ({sel_year - 1})"
        )

    with met2:
        diff = num_of_artists_listened(df, sel_year) - num_of_artists_listened(df, sel_year - 1)
        st.metric(
            label=f"Number of artists listened ({sel_year})",
            value=f"{num_of_artists_listened(df, sel_year):.0f}",
            delta=f"{diff:+,.1f} ({sel_year - 1})"
        )

    with met3:
        diff = get_total_days(df, sel_year) - get_total_days(df, sel_year - 1)
        st.metric(
            label="Total number of days played",
            value=f"{get_total_days(df, sel_year):.1f}",
            delta=f"{diff:+,.1f} days ({sel_year - 1})"
        )

    with met4:
        st.metric(
            label="tba",
            value="76,314",
            delta="-18.4% from previous week"
        )