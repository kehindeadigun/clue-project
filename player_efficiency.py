from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, between, text, func
import pandas as pd
from create_db import Base, Teams, Players, TeamPlayers, Rankings, Games, Details
from datetime import datetime, timedelta

engine = create_engine('sqlite:///testdb.db')
Base.metadata.bind = engine
db = sessionmaker(bind=engine)
session = db()

def get_weeks(season=None):
    """
    Calculates the spread of weeks and returns and index iterable.
    Iterable contains the start of each week
    Args:
    start_year str: A year in string format
    end_year str:  A year in string format
    Returns:
    Weeks : pandas Index of dates.
    """
    if (season is None):
        query = session.query(Games, func.min(Games.game_date_est).label('min'), \
                                          func.max(Games.game_date_est).label('max'))\
                                          .first()
        dates = [query.min, query.max]
        weeks = pd.date_range(*dates,freq="W").strftime('%Y-%m-%d')
    else:
        query = session.query(Games, func.min(Games.game_date_est).label('min'), \
                                          func.max(Games.game_date_est).label('max'))\
                                        .filter(Games.season==season) \
                                        .first()
        dates = [query.min, query.max]
        weeks = pd.date_range(*dates, freq="W").strftime('%Y-%m-%d')
    return weeks

def calc_player_efficiency(season=None, print_result=True):
    """Connects to a database and queries for player efficiency.
    Args:
    season str:  A year in string format
    print_result Bool: True of False. Determines if a command is printed to the screen
    Returns:
        result = A pandas Dataframe of efficiency results
    """
    weeks = get_weeks(season)
    results = ['player_id','efficiency','player_name','week_start','week_end']
    if print_result:
        show_results(results)
    for idx in range(len(weeks)-1):
        best_play = calc_best_play(weeks[idx], weeks[idx+1])
        #expect error when team or result defaults
        if best_play != None:
            player_info = session.query(Players).filter(Players.player_id==best_play.player_id).first()
            player_name = player_info.player_name if player_info else 'Name Unknown'
            result = [player_name, best_play.player_id, best_play.efficiency, weeks[idx], weeks[idx+1]]
            if print_result:
                show_results(result)
            results.append(result)
    return results

def calc_best_play(week_start, week_close):
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

    subq = session.query(Games, Details) \
            .join(Details, Games.game_id==Details.game_id) \
            .filter(between(Games.game_date_est, week_start, \
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
    calc_player_efficiency(print_result=True)