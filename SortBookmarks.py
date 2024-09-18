class RedditBookmarkManager:
    def __init__(self, conn, cursor, reddit):

        self.conn = conn
        self.cursor = cursor
        self.reddit = reddit
        self.bookmarks = []
        self.count = 0

    def fetch_subreddit_for_bookmarks(self, bookmarks_dict):

        for bookmark in bookmarks_dict:
            try:
                search_results = self.reddit.submission(url=bookmark['url'])
                sub_name = search_results.subreddit.display_name
                print(sub_name)
                bookmark['sub'] = sub_name

                self.count += 1
                print(f"Bookmark {self.count} - Subreddit: {sub_name}")
            except Exception as e:
                print(f"{bookmark['url']} is not available: {e}")

        self.bookmarks = bookmarks_dict

    def find_or_create_reddit_folder(self):
        find_reddit_folder_query = "SELECT id FROM moz_bookmarks WHERE title = 'reddit' and type = 2"
        self.cursor.execute(find_reddit_folder_query)
        reddit_folder = self.cursor.fetchall()

        if reddit_folder:
            return reddit_folder[0][0]
        else:
            print("Reddit folder not found.")
            return None

    def organise_bookmarks(self):

        reddit_folder_id = self.find_or_create_reddit_folder()

        if reddit_folder_id is None:
            print("Reddit folder does not exist. Exiting.")
            return

        for bookmark in self.bookmarks:
            try:
                # Check if the subreddit folder already exists
                sub_folder_query = f"""
                    SELECT b.id
                    FROM moz_bookmarks b
                    WHERE b.title = '{bookmark['sub'].replace("'", "''")}' AND b.type = 2
                """
                self.cursor.execute(sub_folder_query)
                folder_id = self.cursor.fetchone()

                if folder_id:
                    folder_id = folder_id[0]
                else:
                    folder_id = self.create_subreddit_folder(bookmark['sub'], reddit_folder_id)

                # Move the bookmark to the appropriate subreddit folder
                if folder_id:
                    update_query = f"""
                        UPDATE moz_bookmarks
                        SET parent = {folder_id}
                        WHERE id = {bookmark['id']};
                    """
                    self.cursor.execute(update_query)
                    self.conn.commit()

            except Exception as e:
                print(f"An error occurred while updating or creating bookmarks: {e}")

    def create_subreddit_folder(self, subreddit, reddit_folder_id):
        # Create a new folder for the subreddit
        print(subreddit)
        try:
            create_folder_query = f"""
                INSERT INTO moz_bookmarks (type, fk, parent, position, title, dateAdded, lastModified, guid, syncStatus)
                VALUES (
                    2, 
                    NULL, 
                    {reddit_folder_id}, 
                    (SELECT IFNULL(MAX(position), 0) + 1 FROM moz_bookmarks WHERE parent = {reddit_folder_id}), 
                    '{subreddit.replace("'", "''")}', 
                    strftime('%s', 'now') * 1000000, 
                    strftime('%s', 'now') * 1000000, 
                    hex(randomblob(12)), 
                    1
                );
            """
            print("Executing Create Folder Query:\n", create_folder_query)
            self.cursor.execute(create_folder_query)
            self.conn.commit()

            # Fetch the newly created folder ID
            sub_folder_query = f"""
                SELECT b.id
                FROM moz_bookmarks b
                WHERE b.title = '{subreddit.replace("'", "''")}' AND b.type = 2;
            """
            self.cursor.execute(sub_folder_query)
            folder_id = self.cursor.fetchone()

            if folder_id:
                return folder_id[0]
            else:
                print(f"Failed to create folder for subreddit: {subreddit}")
                return None

        except Exception as e:
            print("folder was not created as it exists or there was an error")
            return None