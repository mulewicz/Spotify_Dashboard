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

def shared():

    col1, = st.columns(1)
    with col1:

        data_ola['ts_date'] = pd.to_datetime(data_ola['ts_date'])
        data_maciek['ts_date'] = pd.to_datetime(data_maciek['ts_date'])
        available_years = sorted(data_ola['ts_date'].dt.year.unique(), reverse=True)
        year = st.selectbox("Year", available_years)

    tab_type = [['master_metadata_album_artist_name', 'master_metadata_track_name'],
                ['master_metadata_album_artist_name'],
                ['master_metadata_album_artist_name', 'master_metadata_album_album_name']]

    top_left, top_right = st.columns(2)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    bottom_left, bottom_right = st.columns(2)

    for i in range(3):

        shared_songs = shared_tab(data_ola, data_maciek, tab_type[i], year)

        for index, row in shared_songs.reset_index(drop=True).iterrows():
            rank = index + 1

            if i == 1:
                if index < 5:
                    current_col = top_left
                else:
                    current_col = top_right
            elif i == 0:
                current_col = bottom_left
            else:
                current_col = bottom_right

            with current_col:
                mins_a = row['minutes_a']
                mins_b = row['minutes_b']

                if tab_type[i] == ['master_metadata_album_artist_name', 'master_metadata_track_name']:
                    title = row['master_metadata_track_name']
                    artist = row['master_metadata_album_artist_name']
                elif tab_type[i] == ['master_metadata_album_artist_name']:
                    title = row['master_metadata_album_artist_name']
                    artist = ""
                else:
                    title = row['master_metadata_album_album_name']
                    artist = row['master_metadata_album_artist_name']

                rank_color = "#fff"
                color_ola = colors_ola[3]
                color_maciek = colors_maciek[3]

                st.markdown(f"""
                  <div style="
                      background-color: #11141d;
                      border-radius: 10px;
                      padding: 10px 15px;
                      margin-bottom: 8px;
                      display: flex;
                      align-items: center;
                      justify-content: space-between;
                  ">
                      <div style="display: flex; align-items: center; gap: 15px;">
                          <span style="font-size: 1.2rem; font-weight: bold; color: {rank_color}; width: 30px;">#{rank}</span>
                          <div>
                              <div style="color: white; font-weight: 600; font-size: 0.95rem;">{title}</div>
                              <div style="color: #8f9bb3; font-size: 0.8rem;">{artist}</div>
                          </div>
                      </div>
                      <div style="display: flex; gap: 10px;">
                          <div style="font-family: monospace; color: {color_ola}; font-size: 0.9rem; background: #262730; padding: 2px 8px; border-radius: 6px;">
                              {mins_a}
                          </div>
                          <div style="font-family: monospace; color: {color_maciek}; font-size: 0.9rem; background: #262730; padding: 2px 8px; border-radius: 6px;">
                              {mins_b}
                          </div>
                      </div>    
                  </div>
                  """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="tba",
            value="975,124",
            delta="+42.8% "
        )

    with col2:
        st.metric(
            label="tba",
            value="296,241",
            delta="+26.3% "
        )

    with col3:
        st.metric(
            label="tba",
            value="121,908",
            delta="+8.1%"
        )

    with col4:
        st.metric(
            label="tba",
            value="76,314",
            delta="-18.4% from previous week"
        )