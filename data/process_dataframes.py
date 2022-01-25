import pandas as pd
import numpy as np

def process_teams_data(dataframe):
    """Cleans a teams.csv dataset and returns a dataframe
    Args:
    df pandas.Dataframe: A pandas dataframe to clean
    Returns:
    A cleaned pandas dataframe.
    """
    cols = ['TEAM_ID','LEAGUE_ID'] + list(dataframe.columns)[2:]
    dataframe = dataframe.reindex(columns=cols)
    dataframe = dataframe.drop(columns=['YEARFOUNDED'])
    dataframe = dataframe.rename(columns={'TEAM_ID': 'team_id',
                      'LEAGUE_ID': 'league_id',
                      'MIN_YEAR': 'min_year',
                      'MAX_YEAR': 'max_year',
                      'ABBREVIATION': 'abbreviation',
                      'NICKNAME': 'nickname',
                      'CITY': 'city',
                      'ARENA': 'arena',
                      'ARENACAPACITY': 'arena_capacity',
                      'OWNER': 'owner',
                      'GENERALMANAGER': 'generalmanager',
                      'HEADCOACH': 'headcoach',
                      'DLEAGUEAFFILIATION': 'd_league_affiliation'})
    return dataframe


def process_players_data(dataframe):
    """Cleans a players.csv dataset and returns a list of dataframes
    Args:
    df pandas.Dataframe: A pandas dataframe to clean
    Returns:
    A list of two cleaned pandas dataframes.
    list: [pandas.Dataframe for players,pandas.Dataframe for team players]
    """
    cols = ['PLAYER_ID','TEAM_ID','PLAYER_NAME','SEASON']
    dataframe = dataframe.reindex(columns=cols)
    dataframe = dataframe.rename(columns={'PLAYER_ID': 'player_id',
                                  'PLAYER_NAME':'player_name',
                                  'TEAM_ID': 'team_id',
                                  'SEASON': 'season'})
    team_players_df = dataframe.drop(columns=['player_name'])

    players_df = dataframe.drop(columns=['season','team_id'])
    players_df.drop_duplicates(inplace=True)

    return [players_df, team_players_df]


def process_ranking_data(dataframe):
    """Cleans a ranking.csv dataset and returns a dataframe
    Args:
    df pandas.Dataframe: A pandas dataframe to clean
    Returns:
    A cleaned pandas dataframe.
    """
    dataframe.drop(columns=['LEAGUE_ID','TEAM','W_PCT'], inplace=True)
    dataframe.STANDINGSDATE = pd.to_datetime(dataframe.STANDINGSDATE, format='%Y-%m-%d')
    dataframe = dataframe.rename(columns={'TEAM_ID': 'team_id','SEASON_ID': 'season_id',
                          'STANDINGSDATE': 'standings_date','CONFERENCE': 'conference',
                          'G': 'games','W': 'wins',
                          'L': 'loses','HOME_RECORD': 'home_record',
                          'ROAD_RECORD': 'road_record','RETURNTOPLAY': 'return_to_play'})
    return dataframe


def process_games_data(dataframe):
    """Cleans a games.csv dataset and returns a dataframe
    Args:
    df pandas.Dataframe: A pandas dataframe to clean
    Returns:
    A cleaned pandas dataframe.
    """
    cols = ['GAME_ID','GAME_DATE_EST','HOME_TEAM_ID','VISITOR_TEAM_ID','GAME_STATUS_TEXT','SEASON']
    dataframe.drop(columns =['TEAM_ID_home','PTS_home','FG_PCT_home','FG_PCT_home',
                     'FG_PCT_home','FT_PCT_home','FG3_PCT_home','AST_home',
                     'REB_home','TEAM_ID_away','PTS_away','FG_PCT_away','FT_PCT_away',
                     'FG3_PCT_away','AST_away','REB_away','HOME_TEAM_WINS'], inplace=True)
    dataframe.GAME_DATE_EST = pd.to_datetime(dataframe.GAME_DATE_EST, format='%Y-%m-%d')
    dataframe = dataframe.reindex(columns=cols)
    dataframe = dataframe.rename(columns=({'GAME_ID': 'game_id',
                    'GAME_DATE_EST': 'game_date_est',
                    'HOME_TEAM_ID': 'home_team_id',
                    'VISITOR_TEAM_ID': 'visitor_team_id',
                    'GAME_STATUS_TEXT': 'game_status_text',
                    'SEASON': 'season'}))
    return dataframe

def process_details_data(dataframe):
    """Cleans a ranking.csv dataset and returns a dataframe
    Args:
    df pandas.Dataframe: A pandas dataframe to clean
    Returns:
    A cleaned pandas dataframe.
    """
    dataframe.drop(columns =['TEAM_ID','TEAM_ABBREVIATION','TEAM_CITY',\
                             'PLAYER_NAME', 'START_POSITION',\
                             'FG_PCT','FT_PCT','FG3_PCT','REB'], inplace=True)
    dataframe['COMMENT'] = dataframe.COMMENT.str.strip()
    dataframe = dataframe.rename(columns={'GAME_ID': 'game_id',
                            'PLAYER_ID': 'player_id','COMMENT': 'comment',
                            'MIN': 'minute','FGM': 'field_g_made','FGA': 'field_g_attempts',
                            'FG3M': 'field_g3_made', 'FG3A': 'field_g3_attempts',
                            'FTM': 'free_throws_made','FTA': 'free_throw_attempts',
                            'OREB': 'off_rebound','DREB': 'def_rebound','AST': 'assist',
                            'STL': 'steal', 'BLK': 'block','TO': 'turnover',
                            'PF': 'personal_foul','PTS':'points','PLUS_MINUS': 'plus_minus'})
    return dataframe
