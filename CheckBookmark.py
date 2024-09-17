class CheckBookmark:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.results = []

    def check_permalinks_in_db(self, permalinks_batch):

        like_conditions = ' OR '.join([f"p.url LIKE ?" for _ in permalinks_batch])
        query = f"""
        SELECT p.url
        FROM moz_places p
        JOIN moz_bookmarks b ON p.id = b.fk 
        WHERE {like_conditions}
        """

        like_patterns = [f"%{url}%" for url in permalinks_batch]
        self.cursor.execute(query, like_patterns)
        return self.cursor.fetchall()

    def find_matching_urls(self, permalinks):
        batch_size = 30

        # Loop through the permalinks in batches
        for i in range(0, len(permalinks), batch_size):
            batch = permalinks[i:i + batch_size]
            batch_results = self.check_permalinks_in_db(batch)
            self.results.extend(batch_results)

        found_urls = set(result[0] for result in self.results)
        return found_urls