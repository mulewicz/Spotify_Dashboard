import streamlit as st
import pickle
import os

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CORE_DIR, "../../"))

DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
STYLE_PATH = os.path.join(ASSETS_DIR, "style.css")

MAPBOX_TOKEN = st.secrets["MAPBOX_TOKEN"]
SPOTIPY_CLIENT_ID = st.secrets["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = st.secrets["SPOTIPY_CLIENT_SECRET"]
GENIUS_ACCESS_TOKEN = st.secrets["GENIUS_ACCESS_TOKEN"]

PATH_OLA = os.path.join(DATA_DIR, "dane_ola.pkl")
PATH_MACIEK = os.path.join(DATA_DIR, "dane_maciek.pkl")

PATH_LOC_OLA = os.path.join(DATA_DIR, "artist_loc_ola.csv")
PATH_LOC_MACIEK = os.path.join(DATA_DIR, "artist_loc_maciek.csv")
PATH_COUNTRIES = os.path.join(DATA_DIR, "Countries by continents.csv")

with open(PATH_OLA, 'rb') as file:
    data_ola = pickle.load(file)

with open(PATH_MACIEK, 'rb') as file:
    data_maciek = pickle.load(file)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

colors_maciek = ['#1d2026', '#172554', '#1e40af', '#3b82f6', '#60a5fa', '#93c5fd']
colors_ola = ['#1d2026', '#2e1065', '#7c3aed', '#c084fc', '#e9d5ff', '#dcd0ff']
colors_maciek_light = ['#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe', "#008080", "#b2d8d8", "#005b96", "#92d2f9",
                       "#344771"] * 20
colors_ola_light = ['#a78bfa', '#c084fc', '#e9d5ff', '#f3e8ff', "#9F2B68", "#D8BFD8", "#660066", "#800080",
                    "#9f72ca"] * 20