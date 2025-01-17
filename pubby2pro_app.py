import os
import streamlit as st
import pandas as pd
from datetime import datetime

from nba_api_df_org import get_nba_advanced_stats

data_dir = 'data'
current_date = datetime.now().strftime('%b %d, %Y')

if not os.path.exists(data_dir):
    # Make the data folder
    os.makedirs(data_dir)

st.set_page_config(layout="wide")

st.title('From Pubby to Pro')

# Create a horizontal layout with two columns
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader('NBA Advanced Player Stats')

with col2:
    st.subheader(f'{current_date}')

season_id = '2024-25'
season_file_name = f'{data_dir}/nba_advanced_stats_{season_id}.csv'

if not os.path.exists(season_file_name):
    with st.spinner(text = 'Downloading latest data from nba.com'):
        advance_stats_df = get_nba_advanced_stats(season_id)

    advance_stats_df.to_csv(season_file_name, index=False)
else:
    advance_stats_df = pd.read_csv(season_file_name)


st.write(f'There are {advance_stats_df.shape[0]} active players in the following table')
st.dataframe(advance_stats_df)
