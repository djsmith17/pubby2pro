import os
import streamlit as st
import pandas as pd

from nba_api_df_org import get_nba_advanced_stats

data_dir = 'data'

if not os.path.exists(data_dir):
    # Make the data folder
    os.makedirs(data_dir)

st.title('From Pubby to Pro')
st.subheader('NBA Advanced Player Stats')

season_id = '2024-25'
season_file_name = f'{data_dir}/nba_advanced_stats_{season_id}.csv'

if not os.path.exists(season_file_name):
    with st.spinner(text = 'Downloading latest data from nba.com'):
        advance_stats_df = get_nba_advanced_stats(season_id)

    advance_stats_df.to_csv(season_file_name, index=True)
else:
    advance_stats_df = pd.read_csv(season_file_name)

st.dataframe(advance_stats_df)
