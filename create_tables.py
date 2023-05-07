import psycopg2
from sql_queries import create_table_queries, drop_table_queries


class table_creation():

    def create_database(self):
        """
        - Creates and connects to the streamingdb
        - Returns the connection and cursor to streamingdb
        """

        # connect to default database
        self.conn = psycopg2.connect("host=127.0.0.1 dbname=postgres")
        self.conn.set_session(autocommit=True)
        self.cur = self.conn.cursor()

        # create sparkify database with UTF8 encoding
        self.cur.execute("DROP DATABASE IF EXISTS streamingdb")
        self.cur.execute("CREATE DATABASE streamingdb WITH ENCODING 'utf8' TEMPLATE template0")

        # close connection to default database
        self.conn.close()

        # connect to sparkify database
        self.conn = psycopg2.connect("host=127.0.0.1 dbname=streamingdb")
        self.cur = self.conn.cursor()

        return self.cur, self.conn


    def drop_tables(self, cur, conn):
        """
        Drops each table using the queries in `drop_table_queries` list.
        """
        self.cur = cur
        self.conn = conn
        for query in drop_table_queries:
            self.cur.execute(query)
            self.conn.commit()


    def create_tables(self, cur, conn):
        """
        Creates each table using the queries in `create_table_queries` list.
        """
        self.cur = cur
        self.conn = conn
        for query in create_table_queries:
            self.cur.execute(query)
            self.conn.commit()


x = table_creation()
cur, conn = x.create_database()
x.drop_tables(cur,conn)
x.create_tables(cur,conn)
