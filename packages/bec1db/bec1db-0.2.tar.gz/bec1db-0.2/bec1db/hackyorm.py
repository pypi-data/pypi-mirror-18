## Imports
import re
import sqlite3

###-------------------
###  SQLITE functions
###-------------------
class Zeus:
    def __init__(self, databasepath):
        self.databasepath = databasepath


    ## Put a dictionary array into the database
    def insert_dictionary(self, dict_array):

        # Connect to the DB
        conn = sqlite3.connect(self.databasepath)
        cur = conn.cursor()
        images_added = 0

        # Iterate over the dictionary array
        for dict in dict_array:

            # Add the necessary columns. Never delete columns!
            cur.execute('SELECT * FROM data')
            db_columns = [description[0].lower() for description in cur.description]
            dict_columns = [column.lower() for column in list(dict.keys())]
            columns_needed = set(dict_columns)-set(db_columns) # Find the missing keys (columns)
            for column in list(columns_needed):
                sql = 'ALTER TABLE data ADD "{col_name}" FLOAT'
                cur.execute(sql.format(col_name=column)) # Add all the missing keys


            # Save the data
            sql = 'INSERT INTO data ({fields}) VALUES ({values})'
            fields = ", ".join(dict.keys())
            values = ', '.join(['"{0}"'.format(value) for value in dict.values()])
            composed_sql = sql.format(fields=fields, values=values)
            try:
                cur.execute(composed_sql)
            except sqlite3.IntegrityError:
                print('Attemped to add a duplicate')
                images_added -= 1
                pass

            # Count images added
            images_added += 1

        print(str(images_added) +' images added to database')
        conn.commit()
        conn.close()

    ## Query the database
    def data_query(self, sql_query):
        conn = sqlite3.connect(self.databasepath)
        c = conn.cursor()
        c.execute(sql_query)
        result = c.fetchall()
        conn.close()
        return result

    ## Obliterate and re-make the data table
    def data_obliterate(self):
        conn = sqlite3.connect(self.databasepath)
        c = conn.cursor()
        c.execute('''DROP TABLE IF EXISTS data''')
        c.execute('''CREATE TABLE data
                      (snippet_time text UNIQUE, Date text, Time text,
                      year INT, month INT, day INT,
                      hour INT, minute INT, second INT, unixtime INT)''')
        conn.commit()
        conn.close()
