import sqlite3
from decimal import Decimal
from datetime import datetime, timedelta
import json


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Convert Decimal objects to strings to maintain precision
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class DatabaseWrapper:
    def __init__(self, db_path="data.db", setup=True):
        self.__database_path = db_path
        if ".db" not in str(self.__database_path):
            self.__database_path = str(self.__database_path) + "/data.db"
        if setup:
            print("A new table is constructed")
            self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.__database_path)
        cursor = conn.cursor()
        conn = sqlite3.connect(self.__database_path)
        cursor = conn.cursor()
        cursor.execute('''DROP TABLE IF EXISTS link_segments''')
        # Create a new table with the updated schema
        cursor.execute('''CREATE TABLE link_segments
                                  (link_id TEXT, day TEXT, month TEXT, year TEXT, is_weekday BOOLEAN,
                                   is_public_holidays BOOLEAN, is_school_holidays BOOLEAN,
                                    time_sets TEXT, average_travel_times TEXT)''')
        conn.commit()
        conn.close()

    def insert_into_database(self, links_segments_list_dict):
        conn = sqlite3.connect(self.__database_path)
        cursor = conn.cursor()
        for key, time_set_average_travel_time_list_list in links_segments_list_dict.items():
            for time_set_average_travel_time_list in time_set_average_travel_time_list_list:
                for time_set, average_travel_time in time_set_average_travel_time_list:
                    # Unpack the key tuple
                    link_id, day, month, year, is_weekday, is_public_holidays, is_school_holidays = key
                    cursor.execute('''INSERT INTO link_segments (
                                    link_id, day, month, year, is_weekday, is_public_holidays, is_school_holidays,
                                     time_sets, average_travel_times
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        link_id, day, month, year, is_weekday, is_public_holidays, is_school_holidays,
                        time_set, str(average_travel_time)))

        conn.commit()
        conn.close()

    def fetch_all_segment_data(self):  # Connect to the SQLite database
        conn = sqlite3.connect(self.__database_path)
        c = conn.cursor()

        # Execute a query to fetch all rows from the segment_data table
        c.execute('SELECT * FROM link_segments')
        # column_name = 'link_id'
        # specific_value = '0469-0415'
        #
        # c.execute(f"SELECT * FROM link_segments WHERE {column_name} = ?", (specific_value,))

        # Fetch all results
        all_rows = c.fetchall()

        # Close the database connection
        conn.close()

        result_dict = {}
        for row in all_rows:
            key = (row[0], row[1], row[2], row[3], row[4], row[5],
                   row[6])  # link_id, day, month, year, is_weekday, is_public_holidays, is_school_holidays
            time_set, average_travel_time = row[7], row[8]  # Extract time_set and average_travel_time

            if key not in result_dict:
                result_dict[key] = []

            # Append the (time_set, average_travel_time) tuple to the list for this key
            result_dict[key].append((time_set, float(average_travel_time)))

        return result_dict

    def query_columns(self, columns):
        conn = sqlite3.connect(self.__database_path)
        cursor = conn.cursor()

        cursor.execute('SELECT link_id FROM link_segments')

        all_results = cursor.fetchall()

        # Close the database connection
        conn.close()

        for result in all_results:
            print(result[0])  # Each 'result' is a tuple, with the first item being the data from the column
