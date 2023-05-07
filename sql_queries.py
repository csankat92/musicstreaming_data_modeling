songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS  users"
song_table_drop = "DROP TABLE IF EXISTS  songs"
artist_table_drop = "DROP TABLE IF EXISTS  artists"

# CREATE TABLES

songplay_table_create = (""" CREATE TABLE IF NOT EXISTS songplays(
                                songplay_id SERIAL PRIMARY KEY
                                , start_time timestamp
                                , user_id varchar NOT NULL 
                                , level varchar
                                , song_id varchar 
                                , artist_id varchar
                                , session_id int
                                , location varchar
                                , user_agent varchar)""")

user_table_create = (""" CREATE TABLE IF NOT EXISTS users(
                            userid int PRIMARY KEY
                            , firstName varchar
                            , lastName varchar
                            , gender varchar
                            , level varchar)""")

song_table_create = (""" CREATE TABLE IF NOT EXISTS songs(
                            song_id varchar PRIMARY KEY
                            , title varchar
                            , artist_id varchar
                            , year int
                            , duration float) """)

artist_table_create = (""" CREATE TABLE IF NOT EXISTS artists(
                               artist_id varchar PRIMARY KEY
                               , name varchar
                               , location varchar
                               , latitude float
                               , longitude float ) """)


# INSERT RECORDS

songplay_table_insert = (""" INSERT INTO songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT (songplay_id)
                        DO NOTHING""")

user_table_insert = (""" INSERT INTO users (userId, firstName, lastName, gender, level) 
                            VALUES (%s,%s,%s,%s,%s)
                            ON CONFLICT (userId)
                            DO UPDATE
                            SET firstName = EXCLUDED.firstName
                            , lastName = EXCLUDED.lastName
                            , gender = EXCLUDED.gender
                            , level = EXCLUDED.level
                            """)

song_table_insert = (""" INSERT INTO songs (song_id, title, artist_id, year, duration) 
                            VALUES (%s,%s,%s,%s,%s)
                            ON CONFLICT (song_id)
                            DO UPDATE
                            SET title = EXCLUDED.title
                            , artist_id = EXCLUDED.artist_id
                            , year = EXCLUDED.year
                            , duration = EXCLUDED.duration""")

artist_table_insert = (""" INSERT INTO artists (artist_id, name, location, latitude, longitude) 
                            VALUES (%s,%s,%s,%s,%s)
                            ON CONFLICT (artist_id)
                            DO UPDATE
                            SET name = EXCLUDED.name
                            , location = EXCLUDED.location
                            , latitude = EXCLUDED.latitude
                            , longitude = EXCLUDED.longitude""")

# FIND SONGS

song_select = ("""SELECT song_id, songs.artist_id
                FROM songs
                INNER JOIN artists ON artists.artist_id = songs.artist_id
                WHERE songs.title = %s
                AND artists.name = %s 
                AND songs.duration = %s
                """)

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop]
