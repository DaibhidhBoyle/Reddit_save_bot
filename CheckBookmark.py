from urllib.parse import quote

class CheckBookmark:
    def __init__(self):
        self.results = []

    def check_permalinks_in_db(self, permalinks_batch, cursor):
        # Decode percent-encoded URLs (like %C3%BC to ü)
        decoded_batch = [quote(url, safe=':/') for url in permalinks_batch]

        #builds a where statement of each permalink so we can urls that contain them
        like_conditions = ' OR '.join([f"p.url LIKE ?" for _ in decoded_batch])

        query = f"""
        SELECT p.url
        FROM moz_places p
        JOIN moz_bookmarks b ON p.id = b.fk 
        WHERE {like_conditions}
        """

        like_patterns = [f"%{url}%" for url in decoded_batch]
        cursor.execute(query, like_patterns)
        return cursor.fetchall()

    def find_matching_urls(self, permalinks, cursor):
        batch_size = 30

        # Loop through the permalinks in batches
        for i in range(0, len(permalinks), batch_size):
            batch = permalinks[i:i + batch_size]

            batch_results = self.check_permalinks_in_db(batch, cursor)

            self.results.extend(batch_results)

        found_urls = set(result[0] for result in self.results)
        return found_urls
