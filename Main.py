# main.py
import praw
import Secrets

import sqlite3
from pymongo import MongoClient

def main():
    reddit = praw.Reddit(
        client_id=Secrets.secret_info['client_id'],
        client_secret=Secrets.secret_info['client_secret'],
        username=Secrets.secret_info['username'],
        password=Secrets.secret_info['password'],
        user_agent=Secrets.secret_info['user_agent']
    )

    # try:
    #     for saved_item in reddit.user.me().saved(limit=2):
    #         if isinstance(saved_item, praw.models.Submission):
    #             print(f"Title: {saved_item.title}")
    #             print(f"URL: {saved_item.url}\n")
    #             print(f"PERMA: {saved_item.permalink}\n")
    #             print(f"Subreddit: {saved_item.subreddit.display_name}\n")
    #         elif isinstance(saved_item, praw.models.Comment):
    #             print(f"Comment: {saved_item.body}")
    #             print(f"Link: {saved_item.link_url}\n")
    #             print(f"PERMA: {saved_item.permalink}\n")
    #             print(f"Subreddit: {saved_item.subreddit.display_name}\n")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    conn = sqlite3.connect(r"C:\Users\Daibhidh\AppData\Roaming\Mozilla\Firefox\Profiles\wpg9fojf.default-release-1662941926469\places.sqlite")
    cursor = conn.cursor()

    # Check available tables (optional, for your reference)
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print("Tables in SQLite database:", tables)

    # Query to get data from moz_places table (URLs)
    places_query = "SELECT id FROM moz_bookmarks WHERE title = 'reddit'";
    cursor.execute(places_query)
    places_data = cursor.fetchall()

    flattened = [item for sublist in places_data for item in sublist]

    urls = []
    for id in flattened:
        urls_of_reddit_bookmarks_query =  f"""
        SELECT p.url
        FROM moz_bookmarks b
        JOIN moz_places p ON b.fk = p.id
        WHERE b.parent = {id} AND b.type != 2;
        """
        cursor.execute(urls_of_reddit_bookmarks_query)
        booked_urls = cursor.fetchall()

        urls.extend([url[0] for url in booked_urls])

    urls = list(set(urls))
    url_with_sub = []

    for url1 in urls:
        try:
            search_results = reddit.submission(url=url1)
            sub_name = search_results.subreddit.display_name
            url_with_sub.append({"url": url1, "sub": sub_name})

            count += 1
            print(count)
        except:
            print(f"{url1} is not available")





        # for post in search_results:
        #     print(post)


    # places_data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in places_data]
    #
    # # Query to get data from moz_bookmarks table (Bookmarks)
    # bookmarks_query = "SELECT * FROM moz_bookmarks;"
    # cursor.execute(bookmarks_query)
    # bookmarks_data = cursor.fetchall()
    #
    # # Convert the bookmarks data into a list of dictionaries for MongoDB
    # bookmarks_data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in bookmarks_data]
    #
    #
    # conn.close()
    #
    #
    # client = MongoClient("mongodb://localhost:27017/")
    # db = client["firefox_data"]
    #
    #
    # places_collection = db["places"]
    # bookmarks_collection = db["bookmarks"]
    #
    # # Insert data into MongoDB places collection
    # if places_data_list:
    #     places_result = places_collection.insert_many(places_data_list)
    #     print(f"Inserted {len(places_result.inserted_ids)} records into 'places' collection.")
    # else:
    #     print("No records found to insert into 'places' collection.")
    #
    # # Insert data into MongoDB bookmarks collection
    # if bookmarks_data_list:
    #     bookmarks_result = bookmarks_collection.insert_many(bookmarks_data_list)
    #     print(f"Inserted {len(bookmarks_result.inserted_ids)} records into 'bookmarks' collection.")
    # else:
    #     print("No records found to insert into 'bookmarks' collection.")


# C:\Users\Daibhidh\AppData\Roaming\Mozilla\Firefox\Profiles\wpg9fojf.default-release-1662941926469\places.sqlite




if __name__ == "__main__":
    main()