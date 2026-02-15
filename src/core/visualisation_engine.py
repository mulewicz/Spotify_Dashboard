import plotly.express as px
from src.core.analytics import *

def render_shared_artist_timeseries(shared_artists, year, data_ola, data_maciek, freq="D"):
    if shared_artists.empty:
        return

    st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f"""<div class="big-title">Listening over time in {year}</div>""",
        unsafe_allow_html=True
    )

    col_artist, col_who = st.columns([3, 2])

    with col_artist:
        selected_artist = st.selectbox(
            "Choose artist from your shared top:",
            shared_artists['master_metadata_album_artist_name'].tolist(),
            key=f"shared_artist_select_{year}"
        )

    with col_who:
        st.write("Whose listening?")
        who_cols = st.columns(2)
        with who_cols[0]:
            show_ola = st.checkbox("Ola", value=True, key=f"show_ola_{year}")
        with who_cols[1]:
            show_maciek = st.checkbox("Maciek", value=True, key=f"show_maciek_{year}")

    ts_ola = get_artist_timeseries(data_ola, selected_artist, year, freq=freq)
    ts_maciek = get_artist_timeseries(data_maciek, selected_artist, year, freq=freq)

    selected_any = show_ola or show_maciek

    if not selected_any:
        st.info("Zaznacz przynajmniej jedną osobę, żeby zobaczyć wykres.")
        return

    if (show_ola and ts_ola.empty) and (show_maciek and ts_maciek.empty):
        st.info("Brak danych o słuchaniu tego artysty w wybranym roku.")
        return

    if not ts_ola.empty:
        ts_ola['minutes_smooth'] = ts_ola['minutes'].rolling(window=7, min_periods=1).mean()

    if not ts_maciek.empty:
        ts_maciek['minutes_smooth'] = ts_maciek['minutes'].rolling(window=7, min_periods=1).mean()
    fig = go.Figure()

    if show_ola and not ts_ola.empty:
        fig.add_trace(
            go.Scatter(
                x=ts_ola['date'],
                y=ts_ola['minutes_smooth'],
                mode="lines",
                name="Ola (7-day Trend)",
                line=dict(
                    color=colors_ola[3],
                    width=3,
                    shape='spline'
                )
            )
        )

    if show_maciek and not ts_maciek.empty:
        fig.add_trace(
            go.Scatter(
                x=ts_maciek['date'],
                y=ts_maciek['minutes_smooth'],
                mode="lines",
                name="Maciek (7-day Trend)",
                line=dict(
                    color=colors_maciek[3],
                    width=3,
                    shape='spline'
                )
            )
        )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Minutes played (7-day Avg)",  # Warto zaznaczyć, że to średnia
        margin={"l": 40, "r": 20, "t": 20, "b": 40},
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)


def plotly_scatter_map(df, map_token, lat, lon, continent_cords, color):

    fig = px.scatter_mapbox(
        df,
        lat=lat,
        lon=lon,
        size_max=15,
        hover_name="Artist",
        hover_data ={
            "lat" : False,
            "lon" : False,
            "Artist" : False
        }
    )
    if continent_cords == dict(lat=35, lon=90):
        zoomed = 2.5
    else:
        zoomed = 3

    fig.update_layout(
        mapbox_style="light",
        hovermode="closest",
        mapbox=dict(
            accesstoken=map_token,
            bearing=0,
            center=continent_cords,
            pitch=90,
            zoom=zoomed,
        ),
        margin={"r": 15, "t": 15, "l": 15, "b": 15},
        height=600
    )

    fig.update_traces(
        marker=dict(color=color)
    )

    return fig


def plotly_bar_chart(df, color, bars_num):

    df_for_fig = df.head(bars_num)

    fig = px.bar(
        df_for_fig,
        x="Country",
        y="Artist",
    )
    fig.update_layout(
        title = "Number of Artists listened in Each Country",
        yaxis=dict(
            title="Number of Artists",
        )
    )
    fig.update_traces(
        marker=dict(color=color)
    )
    return fig


def get_total_days_mins(data):

    if 'mins' not in data.columns:
        data['mins'] = (data['ms_played'] / 60000)
    total_mins = data['mins'].sum()
    total_days = round(total_mins / (24 * 60))

    return total_mins, total_days

def get_top_5_artists_simple(data, num = 5):

    top = data.groupby(['master_metadata_album_artist_name']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)

    return top.head(num)

def get_top_5_songs_simple(data, num = 5):

    top = data.groupby(['master_metadata_track_name', 'master_metadata_album_artist_name']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)

    return top.head(num)


def get_top_5_albums_simple(data, num=5):

    df = data.groupby(['master_metadata_album_album_name', 'master_metadata_album_artist_name']).size().reset_index(
        name='counts').sort_values(by='counts', ascending=False)

    return df.head(num)