import sys
import time
import pandas as pd
import data
import models
import joblib
from player_efficiency import calc_player_efficiency, make_session
from sqlalchemy import create_engine

def validate_input():
    """
    Validates user input against valid values
    """

    pass

def play_player_productivity(session):
    """
    Prints out player player productivity over the course of a season of all time
    Args:
    session obj: A session connection to the database
    """
    print('\nYou are in Home>Productivity\n')
    time.sleep(0.5)
    print('We are analysing player productivity.\n')
    time.sleep(0.5)
    print('Select a season and I will print out the best player each week.\n')
    time.sleep(0.5)
    program_end = False
    while not program_end:
        try:
            prompt = 'Enter a year from 2003 to 2019. Or enter 0 to see productivity every single week. (Or Enter x , X or exit to exit.) Your Input: '
            input_one = input(prompt)
            if input_one in ['x','X','exit']:
                print(f'{input_one} entered. You are exiting Player productivity...')
                time.sleep(1)
                break
            elif (int(input_one) > 2002 and int(input_one) <= 2019):
                print(f'Most productive players each week in {input_one}')
                
                results = calc_player_efficiency(session, int(input_one))
            elif int(input_one) == 0:
                print('Most productive players each week FROM 2003 TO 2019!')
                results  = calc_player_efficiency(session=session)
            else:
                raise ValueError('Invalid Input')
            program_end = True
        except ValueError:
            print('Invalid Input. Pick a year between 2003 and 2019. Or Enter x, X or exit to exit.')
    if results:
        print(' ')
        #prompt = 'Would you like to write the last results to a csv file before leaving? Enter y or Y for yes and any other key for No. Your Input: '
        #print_input = input(prompt)
        #if print_input in ['y','Y']:
        #    df = pd.DataFrame(results[1:], columns=results[0])
        #    df.to_csv('productivity_results',index=False)
        #    print('File written to productivity_results.csv! \n')

def play_game_prediction(session, model):
    """
    Plays a game of basketball prediction between a person 
        on the command line and a classifier
    Args:
    session obj: A session connection to the database
    model : A model/classifier for use in making predictions
    """
    print('\nYou are in Home>Game Prediction\n')
    time.sleep(0.5)
    print('We are making game predictions\n')
    time.sleep(0.5)
    print('Lets set up 3 random games.')
    time.sleep(0.5)
    print('It is you vs our machine. Predict who wins these games.')
    time.sleep(0.5)
    
    score = {'machine':0, 'player':0}

    for i in range(3):
        time.sleep(0.5)

        (inputs, labels , team_home, team_away) = models.load_data(session, True, True)
        print(f'GAME {i+1} || Current Score: Machine:{score["machine"]}, Player:{score["player"]}')

        print(f'Faceoff: {team_home}(HOME) vs {team_away}(AWAY)')
        user_prediction = '123456789'

        while user_prediction not in ['0','1']:
            prompt = f'Who do you think wins? Enter 0 for {team_home} and 1 for {team_away}.'
            user_prediction = input(prompt)
            if user_prediction not in ['0','1']:
                print('Sorry invalid entry. select 0 or 1')

        prediction = model.predict(inputs)[0]
        print(f'Our machine predicts: {get_name(prediction, team_home, team_away)}')
        print(f'You predicted: {get_name(int(user_prediction), team_home, team_away)}')
        time.sleep(0.5)
        
        if prediction==labels[0]:
            score['machine'] += 1
        if int(user_prediction)==labels[0]:
            score['player'] += 1
        print('\n')
        
        print('')
        print(f'The true winner was: {get_name(labels[0], team_home, team_away)}')
        print(f'Score: Machine:{score["machine"]}, Player:{score["player"]}')

        time.sleep(0.5)
    print_winner(score)
    time.sleep(0.5)
    
    print(f'Final Score: Machine:{score["machine"]}, Player:{score["player"]}')
    time.sleep(0.5)

def get_name(prediction, home_team, away_team):
    """Returns the name of a match prediction"""
    if prediction == 0:
        return away_team
    if prediction == 1:
        return home_team

def print_winner(score, print_win=True):
    """Prints the winner of a prediction faceoff
    Args:
    score: A dictionary of integers with keys machine and player 
    """
    if score['player'] > score['machine']:
        prompt = 'Well, you beat our machine hands down.'
    elif score['player'] < score['machine']:
        prompt = 'Sorry, Our machine is just really good. You lost.'
    else:
        prompt = 'It seems we are at an impasse today. May the best man or machine win next time.'
    print(prompt)

#main program file
def main():
    """
    Main File
    """
    setup_args = sys.argv
    print('Starting server......')
    time.sleep(0.5)
    file_types = ['file','file']
    print('Checking for database and classifier......')
    time.sleep(0.5)
    print(setup_args[1:])
    if (len(setup_args) == 3) and data.check_inputs(setup_args[1:], file_types):
        [database_filepath, model_filepath] = setup_args[1:]
        
        print(f'DB path: {database_filepath}')
        time.sleep(0.5)
        print(f'Model path: {model_filepath} \n')
        time.sleep(0.5)
        
        #make a db session connection
        model = joblib.load(model_filepath)
        #pdb.set_trace()

        print('Welcome to NBA Stats!!!\n')
        time.sleep(0.5)
        user_input = '123456789'
        while user_input not in ['x','X','exit']:
            print('You are in the program home.\n')
            time.sleep(0.5)
            prompt='Enter 1 to Analyse player productivity. Enter 2 for match prediction. (Enter x, X or exit.) Your Input: '
            user_input = input(prompt)

            if user_input == '1':
                time.sleep(0.5)
                session = make_session(database_filepath)
                play_player_productivity(session)
                time.sleep(0.5)
                session.close()
                print('\nPlayer productivity closed...Would you like to do more?')
            
            elif user_input == '2':
                time.sleep(0.5)
                #session = make_session(database_filepath)
                engine = create_engine('sqlite:///'+database_filepath)
                play_game_prediction(engine, model)
                time.sleep(0.5)
                print('Game Prediction closed. Would you like to do more?')          


            elif user_input not in ['X','XX','exit']:
                print('Invalid input...Try again.')

        print('Exiting.....')
        time.sleep(0.5)
        print('Thank you for running NBA Stats!')
        time.sleep(0.5)
    else:
        print('Please provide the filepath of the database. ',\
              'as the first argument and the filepath of the pickle file of ', \
              'the saved model as the second argument. \n\nExample: python', \
              'start.py data/mydb.db classifier.pkl \n', \
              'Also ascertain the database exists and the classifier exist')

if __name__ == '__main__':
    main()