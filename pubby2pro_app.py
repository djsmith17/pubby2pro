'''
Main app window for showing off the table
'''

import os
from datetime import datetime
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

from nba_api_df_org import get_nba_advanced_stats

def download_nba_data(season_id):
    '''
    Use API calls to download NBA data
    '''
    with st.spinner(text = 'Downloading latest data from nba.com', show_time=True):
        return get_nba_advanced_stats(season_id)

def access_nba_csv(season_id, redownload_true):
    '''
    Download and/or accessing the nba_stats as a csv
    '''
    data_dir = 'data'

    if not os.path.exists(data_dir):
        # Make the data folder
        os.makedirs(data_dir)

    season_file_name = f'{data_dir}/nba_advanced_stats_{season_id}.csv'

    # Download the latest version of the NBA stats into a csv
    if redownload_true:
        advance_stats_df = download_nba_data(season_id)
        advance_stats_df.to_csv(season_file_name, index=False)

    # Check to see if CSV file exists
    # If it does not exist, download it
    if not os.path.exists(season_file_name):
        advance_stats_df = download_nba_data(season_id)
        advance_stats_df.to_csv(season_file_name, index=False)
    #If the csv file does exist
    else:
        advance_stats_df = pd.read_csv(season_file_name)

    # Get the last modified date of the file
    file_mod_time = os.path.getmtime(season_file_name)
    file_mod_date = datetime.fromtimestamp(file_mod_time).strftime('%b %d, %Y %I:%M %p')

    return advance_stats_df, file_mod_date

def main():
    '''
    Main function for running the app
    '''

    st.set_page_config(layout="wide")
    current_date = datetime.now().strftime('%b %d, %Y')

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
            redownload_true = st.button('Redownload Data')

    # Access the data from the a local CSV file
    advance_stats_df, file_mod_date = access_nba_csv(season_id, redownload_true)

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

    # Add a multiselect widget to select columns to display
    selected_columns = st.multiselect(
        'Select columns to display',
        options=advance_stats_df.columns.tolist(),
        default=advance_stats_df.columns.tolist()
    )

    # Display the dataframe with selected columns
    st.dataframe(advance_stats_df[selected_columns], use_container_width=True)

    st.subheader('Game History')

if __name__ == '__main__':
    main()
