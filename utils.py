# the code for all plotly figures can be found here
from typing import Any

import numpy as np
import plotly.graph_objects as go
import plotly
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
import lyricsgenius
from wordcloud import WordCloud, STOPWORDS
from langdetect import detect, LangDetectException
from collections import Counter
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
GENIUS_ACCESS_TOKEN = "3O6Gergq8PJj06gtdB2sfrFwPdEMCgZzaN1rdjumu8Bwu8GVHZsYYgMzBsxUAxeF"

def get_lang(lyrics_list):
    detected_langs = []
    for text in lyrics_list:
            lang_code = detect(text)
            detected_langs.append(lang_code)
    stats = Counter(detected_langs)
    data = []
    for code, count in stats.items():
        data.append({'code': code, 'count': count})

    df_stats = pd.DataFrame(data).sort_values(by='count', ascending=False)
    return df_stats

def get_lyrics_cloud_plotly(artist_song_pairs, colors, title):
        genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)
        genius.verbose = False
        genius.remove_section_headers = True

        my_stopwords = set(STOPWORDS)
        my_stopwords.update(['feat', 'ft', 'verse', 'chorus', 'intro', 'outro', 'yeah', 'oh', 'la', 'na', 'ooh'])
        lyrics_data = []
        all_lyrics = ""

        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, (artist, song) in enumerate(artist_song_pairs):
            status_text.text(f"Downloading {artist} - {song}...")
            try:
                song_obj = genius.search_song(song, artist)
                if song_obj and song_obj.lyrics:
                    try:
                        lang_detected = detect(song_obj.lyrics)
                    except:
                        lang_detected = "unknown"

                    lyrics_data.append({
                        "text": song_obj.lyrics,
                        "lang": lang_detected
                    })
            except Exception:
                pass

            progress_bar.progress((i + 1) / len(artist_song_pairs))

        progress_bar.empty()
        status_text.empty()
        available_langs = sorted(list(set([item['lang'] for item in lyrics_data])))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<div class="big-title">Word Cloud</div>', unsafe_allow_html=True)
            st.caption(title)

        with col4:
            selected_lang = st.selectbox("Choose language:", available_langs)

        filtered_lyrics = [item['text'] for item in lyrics_data if item['lang'] == selected_lang]
        all_lyrics = " ".join(filtered_lyrics)
        if not all_lyrics:
            return None

        wc = WordCloud(
            width=1000,
            height=800,
            max_words=100,
            stopwords=my_stopwords,
            background_color='black'
        ).generate(all_lyrics)

        words = []
        #colors = []
        x_pos = []
        y_pos = []
        sizes = []
        for item in wc.layout_:
            words.append(item[0][0])
            sizes.append(item[1])
            x_pos.append(item[2][1])
            y_pos.append(item[2][0] * -1)

        word_colors = [random.choice(colors) for _ in words]
        z_pos = [random.randint(-400, 400) for _ in words]

        fig = go.Figure(go.Scatter3d(
            x=x_pos,
            y=y_pos,
            z=z_pos,
            mode='text',
            text=words,
            hoverinfo='text',
            hovertext=[f"Słowo: {w}" for w in words],
            textfont=dict(
                size=sizes,
                color=colors,
                family="Arial"
            )
        ))

        axis_layout = dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            title='',
            showbackground=False,
            visible=False
        )

        fig.update_layout(
            scene=dict(
                xaxis=axis_layout,
                yaxis=axis_layout,
                zaxis=axis_layout,
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            hovermode='closest'
        )

        return fig

def get_artist_image_url(artist_name: str) -> tuple[None, None] | tuple[Any | None, Any, Any]:
    if not artist_name:
        return None, None

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["SPOTIPY_CLIENT_ID"],
            client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
        )
    )

    result = sp.search(q=artist_name, type="artist", limit=1)
    artists = result.get("artists", {}).get("items", [])

    if not artists:
        return None, None

    artist = artists[0]
    images = artist.get("images", [])
    image_url = images[0]["url"] if images else None
    spotify_url = artist["external_urls"]["spotify"]
    return image_url, spotify_url

def get_the_genre(track_url):
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=st.secrets["SPOTIPY_CLIENT_ID"],
            client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
        )
    )
    track_info = sp.track(track_url)

def get_total_days(data, year):
    if 'mins' not in data.columns:
        data['mins'] = (data['ms_played'] / 60000)
    df_curr = data[data['ts_date'].dt.year == year]
    total_mins = df_curr['mins'].sum()
    total_days = total_mins / (24 * 60)

    return total_days

def group_by_month(data, sel_year):
    full_rng = pd.date_range(f'{sel_year}-01-01', f'{sel_year}-12-31')
    df_year = data[data['ts_date'].dt.year == sel_year].copy()
    df_year['mins'] = (df_year['ms_played'] / 60000).round(0)
    df_grouped = pd.DataFrame(df_year.groupby(df_year['ts_date'].dt.normalize())['mins'].sum())
    df_plot = df_grouped.reindex(full_rng,fill_value=0).reset_index(names='date')
    df_plot['mo'] = df_plot['date'].dt.month
    df_plot['d'] = df_plot['date'].dt.dayofweek
    df_plot['w'] = df_plot['date'].dt.strftime('%W').astype(int)
    df_plot['w'] = df_plot['w'] - df_plot.groupby('mo')['w'].transform('min')
    return df_plot

def get_top_5_artists(data, sel_year, view_mode):
    df = data[data['ts_date'].dt.year == sel_year].copy()
    if view_mode in months:
        month_num = months.index(view_mode) + 1
        df = df[df['ts_date'].dt.month == month_num]
        title = f"Top artists of {sel_year} ({view_mode})"
    else:
        title = f"Top artists of {sel_year}"
    df = df.groupby(['master_metadata_album_artist_name']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    return df.head(6), title

def get_top_5_songs(data, sel_year, view_mode, num = 5):
    df = data[data['ts_date'].dt.year == sel_year].copy()
    if view_mode in months:
        month_num = months.index(view_mode) + 1
        df = df[df['ts_date'].dt.month == month_num]
        title = f"Top songs of {sel_year} ({view_mode})"
    else:
        title = f"Top songs of {sel_year}"
    top = df.groupby(['master_metadata_track_name', 'master_metadata_album_artist_name']).size().reset_index(
        name='counts').sort_values(by='counts', ascending=False)
    return top.head(num), title

def get_top_8_albums(data, sel_year, view_mode):
    if view_mode in months:
        month_num = months.index(view_mode) + 1
        data = data[data['ts_date'].dt.month == month_num]
        title = f"Top albums of {sel_year} ({view_mode})"
    else:
        title = f"Top albums of {sel_year}"

    df = data[data['ts_date'].dt.year == sel_year].copy()
    df = df.groupby(['master_metadata_album_album_name', 'master_metadata_album_artist_name']).size().reset_index(
        name='counts').sort_values(by='counts', ascending=False)
    return df.head(12), title

def num_of_artists_listened(data, sel_year):
    df = data[data['ts_date'].dt.year == sel_year].copy()
    df = df.groupby(['master_metadata_album_artist_name']).size().reset_index()
    return df.shape[0]

def get_max_in_the_day(data, sel_year):
    df = data[data['ts_date'].dt.year == sel_year].copy()

    if df.shape[0] == 0:
        return 0
    daily_sum = df.groupby(df['ts_date'].dt.date)['ms_played'].sum()
    daily_sum_df = daily_sum.reset_index(name='total_ms_played').sort_values(by=['total_ms_played'], ascending=False)
    daily_sum_df['hours'] = daily_sum_df['total_ms_played'] / (1000 * 60 * 60)

    return daily_sum_df.iloc[0]['hours']


def chart_sum(data, sel_year, color):
    df = group_by_month(data, sel_year)
    sums = df.groupby('mo')['mins'].sum()
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=months,
        y=sums,
        mode='lines+markers',
        line=dict(color=color, width=3),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title=f"<b>Minutes Listened per Month ({sel_year})</b>",
        title_font_color="white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#a0a0a0"),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        height=400
    )

    fig.update_yaxes(gridcolor='#333', zerolinecolor='#333', rangemode="tozero")
    fig.update_xaxes(gridcolor='#333')

    return fig



def draw_chart(data, colors, sel_year, view_mode):
    df_plot = group_by_month(data, sel_year)

    active_days = data[data['mins'] > 0]['mins']
    q20 = active_days.quantile(0.2)
    q40 = active_days.quantile(0.4)
    q60 = active_days.quantile(0.6)
    q80 = active_days.quantile(0.8)

    def get_col(v):
        if v == 0: return colors[0]
        if v <= q20: return colors[1]
        if v <= q40: return colors[2]
        if v <= q60: return colors[3]
        if v <= q80: return colors[4]
        return colors[5]

    def r_rect(x, y, w, h, r):
        return f"M {x + r},{y} L {x + w - r},{y} Q {x + w},{y} {x + w},{y + r} L {x + w},{y + h - r} Q {x + w},{y + h} {x + w - r},{y + h} L {x + r},{y + h} Q {x},{y + h} {x},{y + h - r} L {x},{y + r} Q {x},{y} {x + r},{y} Z"

    target_mo = [months.index(view_mode) + 1] if view_mode != "Full Year" else range(1, 13)
    rows, cols, height = (1, 1, 500) if view_mode != "Full Year" else (2, 6, 350)
    titles = [months[i - 1] for i in target_mo]

    fig = make_subplots(rows=rows, cols=cols, subplot_titles=titles, vertical_spacing=0.08, horizontal_spacing=0.015)

    for i, m in enumerate(target_mo):
        d_m = df_plot[df_plot['mo'] == m]
        r, c = (1, 1) if len(target_mo) == 1 else (1 if i < 6 else 2, i + 1 if i < 6 else i - 5)
        xref, yref = f'x{"" if (r - 1) * 6 + c == 1 else (r - 1) * 6 + c}', f'y{"" if (r - 1) * 6 + c == 1 else (r - 1) * 6 + c}'

        hx, hy, ht = [], [], []
        for _, row in d_m.iterrows():
            if row['w'] < 6:
                fig.add_shape(type="path", path=r_rect(row['d'] - 0.4, row['w'] - 0.4, 0.8, 0.8, 0.2),
                              fillcolor=get_col(row['mins']), line=dict(width=0), xref=xref, yref=yref, layer="below")
                hx.append(row['d']);
                hy.append(row['w']);
                ht.append(f"<b>{row['date'].strftime('%d %b')}</b><br>{int(row['mins'])} min")

        fig.add_trace(go.Scatter(x=hx, y=hy, mode='markers', marker=dict(size=20, color='rgba(0,0,0,0)'), text=ht,
                                 hoverinfo='text', showlegend=False), row=r, col=c)
        fig.update_xaxes(showticklabels=False, range=[-0.5, 6.5], row=r, col=c);
        fig.update_yaxes(showticklabels=False, autorange="reversed", range=[-0.5, 5.5], row=r, col=c)

    fig.update_layout(
        title_text=f"<b>{sel_year} Activity</b>" if view_mode == "Full Year" else f"<b>{view_mode} {sel_year}</b>",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Arial", color="#a0a0a0"),
        height=height, margin=dict(t=50, b=10, l=10, r=10), showlegend=False)
    fig.update_annotations(font_color=colors[5])
    return fig