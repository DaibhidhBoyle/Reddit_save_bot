class GetUnsortedBookmarks:
    def __init__(self, conn, cursor):

        self.conn = conn
        self.cursor = cursor

    def getMostRecentEntryParent(self):
        most_recent_parent_id_query = """
                SELECT parent
                FROM moz_bookmarks
                ORDER BY dateAdded DESC;
                """
        self.cursor.execute(most_recent_parent_id_query)
        most_recent_parent_id = self.cursor.fetchone()
        if most_recent_parent_id:
            return most_recent_parent_id[0]
        else:
            return None

    def fetch_reddit_bookmarks(self, recent_parent):

        reddit_bookmarks_query = f"""
        SELECT p.url, b.id
        FROM moz_bookmarks b
        JOIN moz_places p ON b.fk = p.id
        WHERE p.url LIKE '%reddit%' AND b.type = 1 and b.parent = {recent_parent};
        """
        self.cursor.execute(reddit_bookmarks_query)
        all_reddit_bookmarks = self.cursor.fetchall()

        cleaned_reddit_bookmarks = list(set(all_reddit_bookmarks))

        bookmarks_dict = [{'url': bookmark[0], 'id': bookmark[1]} for bookmark in cleaned_reddit_bookmarks]

        return bookmarks_dict