# the code for all plotly figures can be found here
import numpy as np
import plotly.graph_objects as go
import plotly
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

def draw_chart(data, colors, sel_year, view_mode):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    full_rng = pd.date_range(f'{sel_year}-01-01', f'{sel_year}-12-31')
    df_plot = data[data['ts_date'].dt.year == sel_year].set_index('ts_date').reindex(full_rng, fill_value=0).reset_index(
        names='date')

    df_plot['mo'] = df_plot['date'].dt.month
    df_plot['d'] = df_plot['date'].dt.dayofweek
    df_plot['w'] = df_plot['date'].dt.strftime('%W').astype(int)
    df_plot['w'] = df_plot['w'] - df_plot.groupby('mo')['w'].transform('min')

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