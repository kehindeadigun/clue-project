# Parsing NBA Statistics
Parsing NBA Statistics

---
## Table Of Contents
 - [Overview](#overview)
 - [Project Structure](#project-structure)
 - [Process Descriptions](#process-descriptions)
 - [Instructions On Running The Project](#instructions-on-running-the-project)


## Overview
In this project, we parse nba data, load into a database and calculate some statistics from our db. Reading in the data from our normalized database we also predict the result of a match between two opponents. Data is made accesible via a command line interface.

As as defined below:
 - Parse NBA statistics provided in the archive files
 - Dump the statistics into a MySQL database in a normalized format
 - Create a user facing functionality to retrieve the following data points:
 - The best player in terms of productivity for each week of the selected season
 - Prediction of a match result between two teams
 - Exterior command line interface


## Project Structure
Project Main Folder
   |--start_app.py  #runs the main app on the command line<br>
   |<br>
   |--data <br>
   |   |--archive.zip #zipped file of data to process <br>
   |   |--process_data.py  #python file for data processing & cleaning <br>
   | <br>
   |--models <br>
   |   |--classifier.pkl.csv #will hold the classifier of the ml model <br>
   |   |--train_classifier.py  #python script to train model on data <br>
   | <br>
   |--README.md <br>
   |--requirements.txt 


## Process Descriptions
The project can be separted into three sections, each with their contributions to the application.

1. **ETL Pipeline**
A Python script, `process_data.py` and `create_db.py`, that runs a data cleaning pipeline that:
 - Create the db with `create_db.py`
 - Loads the archive datasets
 - Merges the two datasets
 - Cleans the data
 - Stores it in a SQLite database

2. **ML Pipeline**
In a Python script, `train_classifier.py`, that runs a machine learning pipeline that:

 - Loads data from the SQLite database
 - Splits the dataset into training and test sets
 - Builds a text processing and machine learning pipeline
 - Trains and tunes a model
 - Exports the final model as a pickle file

3. **ML Pipeline**
In a Python script, `player_efficiency.py`, that calculates stats from the database:
Productivity is defined as: [Efficiency in Basketball Wiki](https://en.wikipedia.org/wiki/Efficiency_(basketball)) 
    (PTS + REB + AST + STL + BLK − (Missed_FG + Missed_FT + TO)) / GP

 - Calculates the player productivity statistics via an sqlalchemy orm
 - Prints the db to the command line
 - Exports the final model as a pickle file


4. **Command Line Application**
A small interactive command line application that enables you in getting stats and data from the Database


## Instructions On Running The Project
1. Run the following commands in the project's root directory to set up the database and classifier model.

    - To run ETL pipeline that cleans data and stores in database
        `python3 data/process_data.py archive.zip my_db.db`
        or `python3 process_data.py path/to/archive.zip path/to/testdb.db`

    - To run ML pipeline that trains classifier and saves to disk
        `python3 models/train_classifier.py data/my_db.db models/classifier.pkl`

2. Run the following command in the app's directory to run the terminal app.
    `python3 start.py testdb.db classifier.pkl`
