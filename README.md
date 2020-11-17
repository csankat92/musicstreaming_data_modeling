## Data Modeling with Postgres Project

#### Project Summary
Sparkify has created a new music streaming application and wants to establish a Postgres DB to house their song and user activity data. The analytics team at Sparkify wants to analyze what songs users are listening to, but do not have a way to query the data. The data is currently resides in two types of JSON files, one type hosting the user_activity data and the other hosting song data. 

As the data engineer assigned to the project my goal is establish the Postgres DB schema and create an ETL pipeline that will pull the json objects into the designed schema.

#### Database Schema Design and Tables
The schema designed is based off of a star schema structure. The schema design has a single fact table (songplay) and four dimensional tables (users, songs, artists and time) that reference columns in the fact table. 

###### Fact Table

- songplays - records in log data associated with song plays i.e. records with page NextSong
  songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
  
###### Dimension Tables

- users - users in the app
  user_id, first_name, last_name, gender, level
  
- songs - in music database
  song_id, title, artist_id, year, duration

- artists in music database
  artist_id, name, location, latitude, longitude

- time - timestamps of records in songplays broken down into specific units
  start_time, hour, day, week, month, year, weekday
  

#### Data Processing/ETL pipeline

1. Create Sparkify Database and Tables
2. Use Pandas to read JSON files
3. Use Pandas to modify data (Ex. Convert unix time into datatime format)
3. Use psycopg2 to insert data into tables

###### Key transformations during data processing

- Filter songplays data to where page is equal to 'NextSong'.
- Timestamps are converted from UNIX time to datetime format using pandas to_datetime method. 

#### Files in the repository

- Data Directory: Contains user activity and music JSON source files.
- sql_queries.py: Python file containing SQL CREATE, INSERT and SELECT statements.
- create_tables.py: Python file that drops and creates tables; Run this script prior to running etl.py as it will 
  reset your tables.
- etl.py: Python file that reads JSON objects, performs data transformations and loads data into tables.
- etl.ipynb: Python notebook that reads a single JSON object, performs data transformations and loads data into tables.
- test.ipynb: Python notebook used to run SELECT statements against database for testing purposes.
- README.md: Markdown file outlining project and code.

#### How to run the project

1. Run create_tables.py in terminal to drop and create the tables.
2. Run etl.py in terminal to load the json objects to the appropriate tables.
3. Open test.ipynb and run queries to validate data has properly loaded.
