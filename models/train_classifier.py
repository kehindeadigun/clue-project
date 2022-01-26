import sys
import re
import joblib
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

from sqlalchemy import create_engine
from os import path

def is_path(filepath, checktype='dir'):
    """Checks if a path or directory exists. 
    
    Args:
    filepath str: A string representing a path or directory.
    checktype str:  A string. Accepts values 'dir' for directory and 'file' for file. Default: 'dir'
    
    Returns:
    A boolean value: true if the path or directory exists and false otherwise.
     
    """
    if checktype == 'dir':
        if not path.isdir(filepath):
            print('WARNING: Save Path does not exist.')
            return False
    if checktype == 'file':
        if not path.isfile(filepath):
            print('WARNING: File path does not exist.')
            return False
    return True


def check_inputs(inputs, file_types):
    """Checks if multiple inputs exist as files or directories. Uses the is_path function. 
    Args:
    inputs list or array of strings: Contains all the directories to check.
    file_types list or array of strings: Contains the expected file type for each input. Each list value should be a string of value 'file' or 'dir'
    Returns:
    A boolean value: true only if the all path or directories exist and false otherwise.
    """
    for i, filepath in enumerate(inputs):
        if not is_path(filepath, file_types[i]):
            return False
    return True

def parse_data(database_filepath, random=False, ret_team_names=False):
    """Parses data from the database and return a joined daframe of parsed game details
    Args:
    database_filepath str: Contains the path to the database
    random If random, parses database for information on only one game:
    ret_team_names If True, parses database for information on team_names and returns a list
               List holds [home_team_name, away_team_name]
    Returns:
    Dataframe Pandas: A pandas dataframe containing information for a give game
    A List: Only returns a tuple of (dataframe, home_team__name, away_team__name) if ret_team_names flag is triggered.
    """
    engine = create_engine('sqlite:///'+database_filepath) 
    if random:
        games = pd.read_sql('SELECT * FROM games ORDER BY RANDOM() LIMIT 1', engine)
        team_details = pd.read_sql(f'''SELECT game_id, team_id,
                SUM(assist) assist,
                SUM(field_g_made) / SUM(field_g_attempts) field_g_pct,
                SUM(field_g3_made) / SUM(field_g3_attempts) field_g3_pct,
                SUM(free_throws_made) / SUM(free_throw_attempts) free_throw_pct,
                SUM(off_rebound) + SUM(def_rebound) rebound,
                SUM(points) points FROM (SELECT * FROM details WHERE game_id={games.game_id[0]})
                GROUP BY game_id, team_id
                ORDER BY game_id;''', engine)
    else:
        games = pd.read_sql('SELECT * FROM games ORDER BY game_id', engine)
        team_details = pd.read_sql('''SELECT game_id, team_id,
                    SUM(assist) assist,
                    SUM(field_g_made) / SUM(field_g_attempts) field_g_pct,
                    SUM(field_g3_made) / SUM(field_g3_attempts) field_g3_pct,
                    SUM(free_throws_made) / SUM(free_throw_attempts) free_throw_pct,
                    SUM(off_rebound) + SUM(def_rebound) rebound,
                    SUM(points) points FROM details
                    GROUP BY game_id, team_id
                    ORDER BY game_id;''', engine)
    home_team_ls = []
    for (_, items) in team_details[['game_id','team_id']].iterrows():
        game_id = items[0]
        team_id = items[1]
        game = games[games['game_id'] == game_id]
        if game.shape[0] > 0: 
            home_team_ls.append((game['home_team_id'] == team_id).sum())
        else: 
            home_team_ls.append(np.nan)

    team_details['home_team'] = home_team_ls
    
    home_team = team_details[team_details['home_team']==1].drop(columns=['home_team']).reset_index()
    away_team = team_details[team_details['home_team']==0].drop(columns=['home_team']).reset_index()
    
    joined_data = home_team.merge(away_team, how='inner', left_on='game_id',
                              right_on='game_id', suffixes = ('_h', '_a'))
    joined_data['home_team_wins'] = (joined_data['points_h'] > joined_data['points_a']).astype(int)
    dataframe = joined_data.copy()
    if ret_team_names:
        team_home = pd.read_sql(f'''SELECT nickname from teams WHERE team_id={dataframe.team_id_h[0]}''', engine)['nickname'][0]
        team_away = pd.read_sql(f'''SELECT nickname from teams WHERE team_id={dataframe.team_id_a[0]}''', engine)['nickname'][0]
        return dataframe, team_home, team_away
    return dataframe


def load_data(database_filepath, random=False, ret_team_names=False):
    """Loads data from a defined filepath
    Args:
    df pandas.Dataframe: A pandas dataframe to save
    database_filename str: A filename for the database name
    Returns:
    X numpy array: numpy Array: contains the message data values.
    Y numpy array: numpy Array: contains the message target values.
    """
    if ret_team_names:
        (dataframe,home,away) = parse_data(database_filepath, random=random, ret_team_names=True)
    else:
        dataframe = parse_data(database_filepath, random=random, ret_team_names=ret_team_names)

    X = dataframe.drop(columns = ['index_h','index_a','team_id_h','team_id_a','points_h', 'points_a','home_team_wins']).values
    Y = dataframe['home_team_wins'].values
    if ret_team_names:
        return X, Y, home, away
    return X, Y

def build_model(classifier, parameters):
    """
    Builds a multioutput text classifcation model. 
    
    Returns:
    A grid search multiclassification model with a randomforest estimator as base
    """
    scaler = StandardScaler()
    imputer = SimpleImputer(missing_values=np.nan, strategy='median')
    pipeline = Pipeline([('imputer', imputer),
                         ('scaler', scaler),
                         ('clf', classifier)
                        ])
    model = GridSearchCV(pipeline, parameters, verbose=1)
    
    return model


def evaluate_model(model, X_train, X_test, Y_train, Y_test):
    """Evaluates the model, printing out a classification report 
    
    Args:
    model: A scikit learn estimator
    X_test numpy array, list or dataframe: Contains test values from the data
    Y_test numpy array, list or dataframe: Contains test values from the target
    category_names numpy array or list: Contains the category name of each target value.
    """
    eval = {}
    start = time.time()
    predictions = model.predict(X_train)
    eval['train_prediction_time'] = [start - time.time()]
    eval['train_f1_score'] = [f1_score(Y_train, predictions)]
    eval['train_acc_score'] = [accuracy_score(Y_train, predictions)]

    start = time.time()
    predictions = model.predict(X_test)
    eval['test_prediction_time'] = [start - time.time()]
    eval['test_f1_score'] = [f1_score(Y_test, predictions)]
    eval['test_acc_score'] = [accuracy_score(Y_test, predictions)]

    grid_results = pd.DataFrame(eval)
    print(grid_results)

def save_model(model, model_filepath=''):
    """Saves an ML model to the the filepath. Extracts and saves the best estimator if presented with a grid search model. Saves file name is 'classifier.pkl'.
    
    Args:
    model A model to save
    model_filepath str: File path to save the model to. (If filepath does not exist, will save to the model to the same folder as the train_classifier script).
    """
    try:
        best_model = model.best_estimator_
    except:
        best_model = model
    joblib.dump(best_model, model_filepath, compress=True)
    
    print('Saved Successfully!')


def main():
    inputs = sys.argv
    if (len(inputs) == 3) and check_inputs(inputs[1:-1], ['file']):
        database_filepath, model_filepath = inputs[1:]
        
        print('Loading data...\n    Database: {}'.format(database_filepath))
        X, Y = load_data(database_filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
        
        parameters = {'clf__n_estimators':list(range(1,30,5)),
                      'clf__criterion':['gini','entropy'],
                      'clf__max_depth':list(range(2,30,1))}
        parameters = {'clf__n_estimators':[1,2]}
             
        classifier = RandomForestClassifier(verbose=1)

        print('Building model...')
        model = build_model(classifier, parameters)
        
        print('Training model...')
        model.fit(X_train, y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_train, X_test, y_train, y_test)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/my_db.db classifier.pkl '\
              'and ascertain the database exists and the save path exists.')

if __name__ == '__main__':
    main()
