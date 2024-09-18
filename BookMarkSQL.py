import sqlite3
from pymongo import MongoClient

class SetupBookmarkSQL:

    def __init__(self, db_path):

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.tables = self.list_tables()

    def list_tables(self):
        tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print("Tables in SQLite database:", tables)

        #this code is incase you wish to visualise the firefox data but as it slows down run time unnessa
        #
        # client = MongoClient('mongodb://localhost:27017/')
        # db = client['firefox_data']
        #
        # def migrate_table_to_mongo(sqlite_table, mongo_collection_name):
        #     self.cursor.execute(f"SELECT * FROM {sqlite_table}")
        #     rows = self.cursor.fetchall()
        #
        #     # Get column names
        #     column_names = [description[0] for description in self.cursor.description]
        #
        #     # Prepare data for MongoDB
        #     documents = []
        #     for row in rows:
        #         doc = {column_names[i]: row[i] for i in range(len(row))}
        #         documents.append(doc)
        #
        #     # Insert data into MongoDB collection
        #     db[mongo_collection_name].insert_many(documents)
        #     print(f"Inserted {len(documents)} records into {mongo_collection_name} collection.")
        #
        # # Migrate the moz_places table to MongoDB
        # migrate_table_to_mongo('moz_places', 'places')
        #
        # # Migrate the moz_bookmarks table to MongoDB
        # migrate_table_to_mongo('moz_bookmarks', 'bookmarks')

        return tables

    def close_connection(self):
        self.cursor.close()
        self.conn.close()