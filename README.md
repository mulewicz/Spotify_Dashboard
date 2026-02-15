# Spotify Dashboard

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify-1DB954?style=for-the-badge&logo=spotify&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

An interactive data visualization platform designed to analyze personal Spotify streaming history. The application compares musical tastes between users (Ola & Maciek), tracks global artist origins, and provides deep insights into listening habits through an intuitive, dark-themed dashboard.

## About this repository

This project started as a tool to explore long-term music trends and discover overlaps in music tastes. It processes extended Spotify streaming history (JSON files) into optimized data formats for real-time analysis. The entire frontend is built with **Streamlit**, featuring custom CSS to mimic a premium dark-mode experience.

## Application Overview

You can find the application running at: https://spotify--stats.streamlit.app

The core of the application is divided into four specialized modules accessible via the sidebar navigation:

* **Home:** A comprehensive overview of listening habits. Features a "Music Activity Calendar" (GitHub-style heatmap), top artist rankings with direct Spotify links, and a **Lyric Word Cloud** powered by the Genius API to analyze the most frequent vocabulary in favorite songs.
* **Shared Analysis:** A comparison engine that identifies common ground between users. It highlights "shared" artists, tracks, and albums, using a **7-day rolling average trend line** to show how mutual interests evolved over time.
* **Artists on the Map:** A geospatial exploration of music. It uses **Mapbox** to pinpoint where artists come from, allowing users to filter by continent and country to see local popularity trends and regional top charts.
* **Wrapped Experience:** A gamified "Wrapped" summary where users can test their knowledge by guessing their top artists/songs before the results are revealed through interactive UI elements.



### Technical Highlights
* **Data Pipeline:** Custom scripts to convert raw Spotify JSON exports into `Pandas` DataFrames, stored as `Pickle` files for high-speed loading.
* **API Integration:** Real-time fetching of artist metadata and imagery via `Spotipy` and automated lyric scraping via `LyricsGenius`.
* **Dynamic Visualization:** Complex interactive charts built with `Plotly` and `Pyplot`, including custom-styled bar charts, maps, and activity calendars.
* **NLP & Language Detection:** Uses `langdetect` to categorize top songs by language before generating linguistic word clouds.

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | Streamlit, Custom CSS |
| **Data Processing** | Pandas, NumPy, Pickle, Glob |
| **External APIs** | Spotify Web API (Spotipy), Genius API |
| **Visualizations** | Plotly (Maps & Charts), Matplotlib (Word Clouds) |
| **Geodata** | Mapbox |

---

### Setup & Installation

1. Clone the repository and install dependencies: `pip install -r requirements.txt`
2. Configure your credentials in `.streamlit/secrets.toml`:
   - `MAPBOX_TOKEN`
   - `SPOTIPY_CLIENT_ID` / `SPOTIPY_CLIENT_SECRET`
   - `GENIUS_ACCESS_TOKEN`
3. Run the application: `streamlit run main.py`
