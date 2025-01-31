import os
import streamlit as st
import pandas as pd
from datetime import datetime

from nba_api_df_org import get_nba_advanced_stats

def download_nba_data(season_id):
    with st.spinner(text = 'Downloading latest data from nba.com'):
        return get_nba_advanced_stats(season_id)

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

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    season_id = st.selectbox('Select Season', options = ['2024-25'])

with col2:
    st.write(' ')
    with st.expander('Data Configuration'):
        st.button('Redownload Data')

season_file_name = f'{data_dir}/nba_advanced_stats_{season_id}.csv'

if not os.path.exists(season_file_name):
    advance_stats_df = download_nba_data(season_id)

    advance_stats_df.to_csv(season_file_name, index=False)
else:
    advance_stats_df = pd.read_csv(season_file_name)

# Get the last modified date of the file
file_mod_time = os.path.getmtime(season_file_name)
file_mod_date = datetime.fromtimestamp(file_mod_time).strftime('%b %d, %Y %I:%M %p')

with col3:
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(f'There are {advance_stats_df.shape[0]} active players in the following table')

# Add right-aligned text above the table
st.markdown(
    f"<div style='text-align: right; color: grey; font-style: italic;'>This dataset was downloaded on {file_mod_date}</div>",
    unsafe_allow_html=True
)
st.dataframe(advance_stats_df)

st.subheader('Game History')
