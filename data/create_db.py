"""
Used for creating a defined mysqlite database using SQL Alchemy.
This module, when run on the terminal takes in 1 extra argument variable.
This specifies the database name, path and its write destination.
"""
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, String, Float, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

#1. Teams Table
class Teams(Base):
    '''An SQL Alchemy class used in creating the teams table'''
    __tablename__ = 'teams'
    team_id = Column(Integer, primary_key=True)
    league_id = Column(Integer)
    min_year = Column(Integer)
    max_year = Column(Integer)
    abbreviation = Column(String(60))
    nickname = Column(String(60))
    city = Column(String(100))
    arena = Column(String(100), nullable=False)
    arena_capacity = Column(Float)
    owner = Column(String(100))
    generalmanager = Column(String(100))
    headcoach = Column(String(100))
    d_league_affiliation = Column(String(100))

#2. Players Table
class Players(Base):
    '''An SQL Alchemy class used in creating the players table'''
    __tablename__ = 'players'
    player_id = Column(String(), nullable=False, primary_key=True)
    player_name = Column(String(60))

#3. TeamPlayers Table
class TeamPlayers(Base):
    '''An SQL Alchemy class used in creating the team players table'''
    __tablename__ = 'team_players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey('players.player_id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.team_id'), nullable=False)
    season = Column(Integer)
    players = relationship(Players)
    teams = relationship(Teams)

#4. Rankings Table
class Rankings(Base):
    '''An SQL Alchemy class used in creating the rankings table'''
    __tablename__ = 'rankings'
    rank_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'))
    season_id = Column(Integer)
    standings_date = Column(Date())
    conference = Column(String(60))
    games = Column(Integer)
    wins = Column(Integer)
    loses = Column(Integer)
    home_record = Column(String(10))
    road_record = Column(String(10))
    return_to_play = Column(String(10))
    teams = relationship(Teams)

#5. Games Table
class Games(Base):
    '''An SQL Alchemy class used in creating the games table'''
    __tablename__ = 'games'
    game_id = Column('game_id', Integer, primary_key=True)
    game_date_est = Column(Date())
    home_team_id = Column(Integer, ForeignKey('teams.team_id'))
    visitor_team_id = Column(Integer, ForeignKey('teams.team_id'))
    game_status_text = Column(String(60))
    season = Column(Integer)
    teams = relationship(Teams)

#6. GamesDetails Table
class GamesDetails(Base):
    '''An SQL Alchemy class used in creating the games_details table'''
    __tablename__ = 'details'
    stat_id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.game_id'))
    player_id = Column(Integer, ForeignKey('players.player_id'))
    comment = Column(String(300), default='Empty Comment')
    minute = Column(String(10))
    field_g_made = Column(Float)
    field_g_attempts = Column(Float)
    field_g3_made = Column(Float)
    field_g3_attempts = Column(Float)
    free_throws_made = Column(Float)
    free_throw_attempts = Column(Float)
    off_rebound = Column(Float)
    def_rebound = Column(Float)
    assist = Column(Float)
    steal = Column(Float)
    block = Column(Float)
    turnover = Column(Float)
    personal_foul = Column(Float)
    points = Column(Float)
    plus_minus = Column(Float)
    games = relationship(Games)
    players = relationship(Players)

def create_database(database_filepath='my_db'):
    '''Main. Creates an SQlite database using SQL alchemy.
    When run on the system, it takes an argument variable.
    Uses this variable to create the database.
    '''
    print('Creating the database....')
    if database_filepath[-3:] != '.db':
        database_filepath+='.db'
    engine = create_engine('sqlite:///'+database_filepath)
    Base.metadata.create_all(engine)
    print(f'database {database_filepath} succesfully created')
    return database_filepath

if __name__ == '__main__':
    create_database()
