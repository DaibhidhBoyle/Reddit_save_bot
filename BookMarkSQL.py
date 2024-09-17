class BookMarkSQLHandler:
    def __init__(self, db_path):
        #r"C:\Users\Daibhidh\AppData\Roaming\Mozilla\Firefox\Profiles\wpg9fojf.default-release-1662941926469\places.sqlite"
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def list_tables(self):
        tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print("Tables in SQLite database:", tables)
        return tables

    def close_connection(self):
        self.cursor.close()
        self.conn.close()