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
            df = pd.DataFrame(results[1:], columns=results[0])
            df.to_csv('productivity_results',index=False)
            print('File written to productivity_results.csv! \n')