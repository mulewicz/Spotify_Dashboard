import pandas as pd
import streamlit as st
import pickle
import os

colors_maciek = ['#1d2026', '#172554', '#1e40af', '#3b82f6', '#60a5fa', '#93c5fd']
colors_ola = ['#1d2026', '#2e1065', '#7c3aed', '#c084fc', '#e9d5ff', '#dcd0ff']
colors_maciek_light = ['#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe', "#008080", "#b2d8d8", "#005b96", "#92d2f9",
                       "#344771"] * 20
colors_ola_light = ['#a78bfa', '#c084fc', '#e9d5ff', '#f3e8ff', "#9F2B68", "#D8BFD8", "#660066", "#800080",
                    "#9f72ca"] * 20
with open('data/dane_ola.pkl', 'rb') as file:
    data_ola = pickle.load(file)

with open('data/dane_maciek.pkl', 'rb') as file:
    data_maciek = pickle.load(file)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STYLE_PATH = os.path.join(BASE_DIR, "style.css")

def shared_tab(data_a, data_b, col, sel_year):
    df_a= data_a[data_a['ts_date'].dt.year == sel_year].copy()
    df_b = data_b[data_b['ts_date'].dt.year == sel_year].copy()
    def filter_time(df):

        clean = df.loc[(df['ms_played'] > 30000) & (df[col[0]].notna()), :]

        grouped = clean.groupby(col)['ms_played'].sum().reset_index()
        grouped['minutes'] = grouped['ms_played'] / 60000
        return grouped.drop(columns=['ms_played'])

    tab_a = filter_time(df_a).rename(columns={'minutes': 'minutes_a'})
    tab_b = filter_time(df_b).rename(columns={'minutes': 'minutes_b'})

    shared = tab_a.merge(tab_b, on=col, how='inner')

    shared['shared_time'] = shared[['minutes_a', 'minutes_b']].min(axis=1)

    res_tab = shared.sort_values('shared_time', ascending=False).head(10)
    return res_tab.round(1)


dane_maciek = pd.read_pickle("data/dane_maciek.pkl")
dane_ola = pd.read_pickle("data/dane_ola.pkl")



