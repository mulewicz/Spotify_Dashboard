import pandas as pd

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


