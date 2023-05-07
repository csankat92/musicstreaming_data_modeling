import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

class etl():

    def connect_to_db(self):
        self.conn = psycopg2.connect("host=127.0.0.1 dbname=streamingdb")
        self.cur = self.conn.cursor()

        return self.conn, self.cur

    def process_song_file(self, cur, filepath):
        """ Loads song JSON file and inserts data
            into songs and artists table

        Arguments:
            cur: cursor used to communicate with DB
            filepath: filepath for song JSON file
        """
        self.cur = cur
        self.filepath = filepath
        self.song_table_insert = song_table_insert
        self.artist_table_insert = artist_table_insert
        # open song file
        self.df = pd.read_json(self.filepath, lines=True)

        # insert song record
        self.song_data = self.df[['song_id', 'title', 'artist_id', 'year', 'duration']].values
        self.song_data = list(self.song_data[0])
        self.cur.execute(self.song_table_insert, self.song_data)

        # insert artist record
        self.artist_data = self.df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values
        self.artist_data = list(self.artist_data[0])
        self.cur.execute(self.artist_table_insert, self.artist_data)


    def process_log_file(self, cur, filepath):
        """ Loads user_activity JSON file and inserts data
            into songplays, users and time table

        Arguments:
            cur: cursor used to communicate with DB
            filepath: filepath for user_activity JSON file
        """
        self.cur = cur
        self.filepath = filepath

        # open log file
        self.df = pd.read_json(self.filepath, lines=True)

        # filter by NextSong action
        self.df = self.df[self.df['page'] == 'NextSong']

        # load user table
        self.user_df = self.df[['userId', 'firstName', 'lastName', 'gender', 'level']]

        # insert user records
        for i, row in self.user_df.iterrows():
            self.cur.execute(user_table_insert, row)

        # insert songplay records
        for index, row in self.df.iterrows():

            # get songid and artistid from song and artist tables
            self.cur.execute(song_select, (row.song, row.artist, row.length))
            self.results = self.cur.fetchone()

            if self.results:
                self.songid, self.artistid = self.results
            else:
                self.songid, self.artistid = None, None

            # insert songplay record
            self.songplay_data = (
            index, pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, self.songid, self.artistid, row.sessionId, row.location,
            row.userAgent)
            self.cur.execute(songplay_table_insert, self.songplay_data)


    def process_data(self, conn, cur, filepath, func):
        """ Identifes each JSON filepath, runs
            the selected function and print file processing status.

        Arguments:
            cur: cursor used to communicate with DB
            conn: connection to DB
            filepath: filepath for JSON files
            func: selected data processing function
        """
        self.conn = conn
        self.cur = cur
        self.filepath = filepath
        self.func = func
        # get all files matching extension from directory
        self.all_files = []
        for root, dirs, files in os.walk(self.filepath):
            self.files = glob.glob(os.path.join(root, '*.json'))
            for f in self.files:
                self.all_files.append(os.path.abspath(f))

        # get total number of files found
        self.num_files = len(self.all_files)
        print('{} files found in {}'.format(self.num_files, self.filepath))

        # iterate over files and process
        for i, datafile in enumerate(self.all_files, 1):
            func(self.cur, datafile)
            self.conn.commit()
            print('{}/{} files processed.'.format(i, self.num_files))

x = etl()
conn, cur = x.connect_to_db()
x.process_data(conn, cur, 'data/song_data', x.process_song_file)
x.process_data(conn, cur, 'data/log_data', x.process_log_file)
