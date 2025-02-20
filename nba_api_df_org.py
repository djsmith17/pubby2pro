'''
Set of functions to download NBA data using
the nba_api
'''

import time
import warnings
import pandas as pd

from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players, teams

# Suppress FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

def get_nba_advanced_stats(season_id):
    '''
    Quick and Dirty funtion for compiling NBA stats
    using nba_api
    '''

    # Dataframe of all active NBA players
    players_list = players.get_active_players()
    players_df = pd.DataFrame(players_list)

    return compile_adv_stats(season_id, players_df)

def compile_adv_stats(season_id, players_df):
    '''
    api calls to compile data from playercareerstats endpoint
    '''

    advanced_stats_df = pd.DataFrame()
    for row, player in players_df.iterrows():

        time.sleep(1.0)
        player_id = player['id']
        career_resp = playercareerstats.PlayerCareerStats(player_id = player_id)
        career_df = pd.DataFrame(career_resp.get_data_frames()[0])

        if season_id in career_df['SEASON_ID'].values:
            career_season = career_df.loc[career_df['SEASON_ID'] == season_id, :]

            # Find Player Real Name
            player_name = players_df.loc[players_df['id'] == player_id, 'full_name'].reset_index(drop= True)
            career_season.loc[:, 'PLAYER_ID'] = player_name[0]

            advanced_stats_df = pd.concat([advanced_stats_df, career_season])

    advanced_stats_df = advanced_stats_df.rename(columns = {'PLAYER_ID': 'Player', 'TEAM_ABBREVIATION': 'Team', 'PLAYER_AGE': 'Age'})
    advanced_stats_df = advanced_stats_df.drop(['SEASON_ID', 'LEAGUE_ID', 'TEAM_ID'], axis = 1).reset_index(drop=True)

    return advanced_stats_df
