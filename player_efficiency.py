import sys
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, between, func
from sqlalchemy.pool import NullPool
import data

def make_session(database_filepath):
    """
    Creates a session connection to a db with sql alchemy
    Args:
    database_filepath: Path to the database
    """
    engine = create_engine('sqlite:///'+database_filepath, poolclass=NullPool)
    data.Base.metadata.bind = engine
    database = sessionmaker(bind=engine)
    session = database()
    return session

def get_weeks(session, season=None):
    """
    Calculates the spread of weeks over a givem period or over all seasons
    Args:
    session: An SQL alchemy session object
    season str:  A season/year in string format'.
    If not sets dates 
    Returns:
    Weeks : pandas Index of dates.
            An iterable of string dates [date1, date2, date3....]
    The string is a date in the format %Y-%m-%d representing the start of a new week.
    """
    if (season is None):
        query = session.query(data.Game, func.min(data.Game.game_date_est).label('min'), \
                                          func.max(data.Game.game_date_est).label('max'))\
                                          .first()
        dates = [query.min, query.max]
        weeks = pd.date_range(*dates,freq="W").strftime('%Y-%m-%d')
    else:
        query = session.query(data.Game, func.min(data.Game.game_date_est).label('min'), \
                                          func.max(data.Game.game_date_est).label('max'))\
                                        .filter(data.Game.season==season) \
                                        .first()
        dates = [query.min, query.max]
        weeks = pd.date_range(*dates, freq="W").strftime('%Y-%m-%d')
    return weeks

def calc_player_efficiency(session, season=None, print_result=True):
    """Connects to a database and queries for player efficiency.
    Args:
    session: An SQL alchemy session object
    season str:  A year in string format
    print_result Bool: True of False. Determines if a command is printed to the screen
    Returns:
    result : A pandas Dataframe: A dataframe containing efficiency results
    """
    weeks = get_weeks(session, season)
    results = ['player_id','efficiency','player_name','week_start','week_end']
    if print_result:
        show_results(results)
    for idx in range(len(weeks)-1):
        best_play = calc_best_play(session, weeks[idx], weeks[idx+1])
        #expect error when team or result defaults
        if best_play != None:
            player_info = session.query(data.Player).filter(data.Player.id==best_play.player_id).first()
            player_name = player_info.player_name if player_info else 'Name Unknown'
            result = [player_name, best_play.player_id, best_play.efficiency, weeks[idx], weeks[idx+1]]
            if print_result:
                show_results(result)
            results.append(result)
    return results

def calc_best_play(session, week_start, week_close):
    """
    Queries the database for player efficiency in a given week.
    Args:
    week_start str: A date string defining the start of the week.
    week_close str: A date string defining the end of the week.
    Returns:
    best_play: An sql alchemy object containing the best play statistics
    """
    week_start = datetime.strptime(week_start, "%Y-%m-%d") - timedelta(days=1)
    week_start =  datetime.strftime(week_start, "%Y-%m-%d")
    week_close = datetime.strptime(week_close, "%Y-%m-%d") + timedelta(days=1) 
    week_close = datetime.strftime(week_close, "%Y-%m-%d")

    subq = session.query(data.Game, data.Statistics) \
            .join(data.Statistics, data.Game.id==data.Statistics.game_id) \
            .filter(between(data.Game.game_date_est, week_start, \
                                                 week_close)) \
            .subquery()

    best_play = session.query(subq, func.round((subq.c.points + subq.c.def_rebound + subq.c.off_rebound + subq.c.assist +
                                subq.c.steal + subq.c.block + subq.c.free_throws_made + subq.c.field_g_made +
                                subq.c.field_g3_made - subq.c.free_throw_attempts - subq.c.field_g_attempts -
                                subq.c.field_g3_attempts - subq.c.turnover) / func.count(subq.c.game_id),2).label('efficiency')) \
                    .group_by(subq.c.player_id) \
                    .order_by(desc('efficiency')) \
                    .limit(1) \
                    .first()
    return best_play

def show_results(iterable, spacing=15):
    """
    Prints the values from an iterable to the command line screen with spacing
    """
    screen_print = '|   '
    for value in iterable:
        value = str(value)
        screen_print += value
        if len(value) < spacing:
            screen_print += ' '*(spacing-len(value)) + '|'
    print(screen_print)

if __name__=='__main__':
    session = make_session()
    calc_player_efficiency(session, print_result=True)
    session.close()