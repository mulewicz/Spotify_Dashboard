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