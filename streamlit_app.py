import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import sys
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
import pickle
colors_maciek = ['#1d2026', '#172554', '#1e40af', '#3b82f6', '#60a5fa', '#93c5fd']
colors_ola = ['#1d2026', '#2e1065', '#7c3aed','#c084fc','#e9d5ff','#dcd0ff']

with open('data/dane_ola.pkl', 'rb') as file:
    data_ola = pickle.load(file)

with open('data/dane_maciek.pkl', 'rb') as file:
    data_maciek = pickle.load(file)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STYLE_PATH = os.path.join(BASE_DIR, "style.css")


st.set_page_config(layout="wide")
st.write("<style>" + open(STYLE_PATH).read() + "</style>", unsafe_allow_html=True)

st.sidebar.title("choose data")
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Stats", "playlists on the map", "generate your own spotify wrapped", "Summary"],
        styles = {"nav-link-selected":{"background-color": "#202035"} }
    )

st.markdown('<div class="big-title">Spotify Dashboard Overview</div>', unsafe_allow_html=True)
st.caption("This app was created to analyse trends present in our music taste")

if selected == "Home":
  col1, col2= st.columns((2,3))

  with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Total time listened</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-value">3,049K minutes</div>', unsafe_allow_html=True)
    st.markdown('<div class="chip"><div class="chip-dot"></div>+100 min compared to 2023</div>', unsafe_allow_html=True)
    st.caption("this adds upp to 120 days")
    st.markdown('</div>', unsafe_allow_html=True)

  with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Our Favourite albums**")

    st.markdown('</div>', unsafe_allow_html=True)

  bottom_left, bottom_right = st.columns((3,2))

  st.title("Music Activity Calendar")
  col1, col2 = st.columns([3, 1])
  with col2:
      sel_person = st.selectbox("Choose user",[ "Maciek", "Ola"])
      if sel_person == "Ola":
          data = data_ola
          colors = colors_ola
      else:
          data = data_maciek
          colors = colors_maciek

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

  with bottom_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("**minutes listened per month (maciek fiolet, ola rozowy)*")
    df = pd.DataFrame({
        "month": ["Jan","Feb","Mar","Apr","May","Jun"],
        "minutes listened": [2200, 2450, 3049, 2800, 2900, 3100]
    })
    fig = px.bar(df, x="month", y="minutes listened")
    fig.update_layout(template="plotly_dark", height=260, margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

  with bottom_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("**Top genre per season**")
    table = pd.DataFrame({
        "Season": ["Spring","Summer","Autumn","Winter"],
        "Ola": ["musicals","rock","indie","alternative"],
        "Maciek": ["rap","alternative","pop","rap"]
    })
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

if selected == "Stats":
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