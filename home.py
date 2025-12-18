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

def home():


    if True:
      col_1, col_2= st.columns((2,3))
      art1, art2 = st.columns([1, 1.5], gap="large")
      st.markdown('<div class="card">', unsafe_allow_html=True)
      st.markdown('<div class="big-title">Music Activity calendar</div>', unsafe_allow_html=True)
      col1, col2 = st.columns([3, 1])
      with col2:
          sel_person = st.selectbox("Choose user",[ "Maciek", "Ola"])
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
          sel_year = st.selectbox("Year", available_years)
          months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
          view_mode = st.selectbox("View", ["Full Year"] + months)

      with col1:
          st.plotly_chart(draw_chart(data, colors, sel_year, view_mode), use_container_width=True)

      with col_1:
          st.markdown('<div class="card">', unsafe_allow_html=True)
          top_artists_df, title = get_top_5_artists(df, sel_year, view_mode)
          st.caption(title)
          rank_color = colors[3]
          for idx, row in top_artists_df.reset_index(drop=True).iterrows():
              rank = idx + 1
              artist_name = row['master_metadata_album_artist_name']
              count = row['counts']
              img_url, spotify_link = get_artist_image_url(artist_name)
              if not img_url: img_url = "https://via.placeholder.com/50"
              html_code = f"""
                    <a href="{spotify_link}" target="_blank" style="text-decoration: none;">
                        <div class="artist-row">
                            <span style="font-size: 1.2rem; font-weight: bold; color: {rank_color}; width: 30px;">#{rank}</span>
                            <img src="{img_url}" class="artist-img">
                            <div class="artist-info">
                                <p class="artist-name">{artist_name}</p>
                                <p class="artist-stats">{count} odtworzeń</p>
                            </div>
                            <div class="spotify-icon">➤</div>
                        </div>
                    </a>
                    """
              st.markdown(html_code, unsafe_allow_html=True)



      with col_2:
          st.markdown('<div class="card">', unsafe_allow_html=True)

          top_albums_df, title = get_top_8_albums(df, sel_year, view_mode)
          st.caption(title)
          cols = st.columns(4)

          for i, (idx, row) in enumerate(top_albums_df.iterrows()):
              album_name = row['master_metadata_album_album_name']
              artist_name = row['master_metadata_album_artist_name']
              cover_url, _ = get_artist_image_url(artist_name)
              if not cover_url: cover_url = "https://via.placeholder.com/150"

              with cols[i % 4]:
                  st.markdown(f"""
                        <div class="album-grid-item">
                            <img src="{cover_url}" class="album-cover">
                            <div class="album-title-text" title="{album_name}">{album_name}</div>
                            <div class="album-artist-text">{artist_name}</div>
                        </div>
                        """, unsafe_allow_html=True)

      bottom_left, bottom_right = st.columns((2,3))
      with bottom_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        fig = chart_sum(data, sel_year, colors[3])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

      with bottom_right:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        top_songs, title = get_top_5_songs(df, sel_year, view_mode)
        st.caption(title)
        for index, row in top_songs.reset_index(drop=True).iterrows():
            rank = index + 1
            title = row['master_metadata_track_name']
            artist = row['master_metadata_album_artist_name']
            plays = row['counts']

            rank_color = colors[3]

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
                <div style="font-family: monospace; color: #ccc; font-size: 0.9rem; background: #262730; padding: 2px 8px; border-radius: 6px;">
                    {plays}
                </div>
            </div>
            """, unsafe_allow_html=True)

      met1, met2, met3, met4 = st.columns(4)

      with met1:
          diff = get_max_in_the_day(df, sel_year) - get_max_in_the_day(df, sel_year-1)
          st.metric(
              label=f"Max hours in a day ({sel_year})",
              value=f"{get_max_in_the_day(df, sel_year):.1f}",
              delta=f"{diff:+,.1f} h ({sel_year-1})"
          )

      with met2:
          diff = num_of_artists_listened(df, sel_year) - num_of_artists_listened(df, sel_year-1)
          st.metric(
              label=f"Number of artists listened ({sel_year})",
              value=f"{num_of_artists_listened(df, sel_year):.0f}",
              delta=f"{diff:+,.1f} ({sel_year-1})"
          )

      with met3:
          diff = get_total_days(df, sel_year) - get_total_days(df, sel_year-1)
          st.metric(
              label="Total number of days played",
              value=f"{get_total_days(df, sel_year):.1f}",
              delta=f"{diff:+,.1f} days ({sel_year-1})"
          )

      with met4:
          st.metric(
              label="tba",
              value="76,314",
              delta="-18.4% from previous week"
          )

          df_top_data, _ = get_top_5_songs(df, sel_year, view_mode, num=10)
          top_songs = list(
              zip(df_top_data['master_metadata_album_artist_name'], df_top_data['master_metadata_track_name']))
      st.markdown('<div class="card">', unsafe_allow_html=True)
      if view_mode == "Full Year":
          title = f"{sel_year}"
      else:
          title = f"{sel_year} ({view_mode})"
      fig = get_lyrics_cloud_plotly(top_songs, colors_light, title)

      if fig:
              st.plotly_chart(fig, use_container_width=True)
      else:
              st.warning("Nie udało się pobrać wystarczającej ilości tekstu.")
