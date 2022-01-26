import sys
import time
from sqlalchemy import create_engine
from process_data import check_inputs
from player_efficiency import calc_player_efficiency
import pandas as pd

def play_player_productivity(database_filepath):
    """
    Description
    """
    print('\nYou are in Home>Productivity\n')
    time.sleep(0.5)
    print('We are analysing player productivity.\n')
    time.sleep(0.5)
    print('Select a season and I will print out the best player each week.\n')
    time.sleep(0.5)
    program_end = False
    while (not program_end):
        try:
            prompt = 'Enter a year from 2003 to 2019. Or enter 0 to see productivity every single week. (Or Enter x , X or exit to exit.) Your Input: '
            input_one = input(prompt)
            if input_one in ['x','X','exit']:
                print(f'{input_one} entered. You are exiting Player productivity...')
                time.sleep(1)
                break
            elif (int(input_one) > 2002 and int(input_one) <= 2019):
                print(f'Most productive players each week in {input_one}')
                results = calc_player_efficiency(int(input_one))
            elif int(input_one) == 0:
                print('Most productive players each week FROM 2003 TO 2019!')
                results  = calc_player_efficiency()
            else:
                raise ValueError('Invalid Input')
            program_end = True
        except ValueError:
            print('Invalid Input. Pick a year between 2003 and 2019. Or Enter x, X or exit to exit.')
    if results:
        print(' ')
        prompt = 'Would you like to write the last results to a csv file before leaving? Enter y or Y for yes and any other key for No. Your Input: '
        print_input = input(prompt)
        if print_input in ['y','Y']:
            data_frame = pd.DataFrame(results[1:], columns=results[0])
            data_frame.to_csv('productivity_results',index=False)
            print('File written to productivity_results.csv! \n')

#main program file
def main():
    setup_args = sys.argv
    print('Starting server......')
    time.sleep(2)
    file_types = ['file','file']
    print('Checking for database and classifier......')
    time.sleep(2)
    if (len(setup_args) == 3) and check_inputs(setup_args[1:], file_types):
        [database_filepath, model_filepath] = setup_args[1:]
        print(f'DB path: {database_filepath}')
        time.sleep(0.6)
        print(f'Model path: {model_filepath} \n')
        time.sleep(2)
        print('Welcome to NBA Stats!!!\n')
        time.sleep(1.5)
        user_input = '53'
        while user_input not in ['x','X','exit']:
            print('You are in the program home.\n')
            time.sleep(1)
            prompt='Enter 1 to Analyse player productivity. Enter 2 for match prediction. (Enter x, X or exit.) Your Input: '
            user_input = input(prompt)

            if user_input == '1':
                time.sleep(1)
                play_player_productivity(database_filepath)
                time.sleep(2)
                print('\nPlayer productivity closed...Would you like to do more?')
            
            elif user_input == '2':
                time.sleep(1)
                play_game_prediction(database_filepath, model_filepath)
                time.sleep(2)
                print('Done with Game Prediction? Would you like to do more?')            


            elif user_input not in ['X','XX','exit']:
                print('Invalid input...Try again.')

        print('Exiting.....')
        time.sleep(1)
        print('Thank you for running NBA Stats!')
        time.sleep(1)  
    else:
        print('Please provide the filepath of the database. ',\
              'as the first argument and the filepath of the pickle file to', \
              'save the model to as the second argument. \n\nExample: python', \
              'train_classifier.py ../data/mydb.db classifier.pkl \n', \
              'Also ascertain the database exists and the classifier exist')

    

if __name__ == '__main__':
    main()