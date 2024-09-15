# main.py
import praw
import Secrets

import sqlite3
from pymongo import MongoClient

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

import pyautogui


def main():
    reddit = praw.Reddit(
        client_id=Secrets.secret_info['client_id'],
        client_secret=Secrets.secret_info['client_secret'],
        username=Secrets.secret_info['username'],
        password=Secrets.secret_info['password'],
        user_agent=Secrets.secret_info['user_agent']
    )

    #
    try:
        for saved_item in reddit.user.me().saved(limit=2):
            if isinstance(saved_item, praw.models.Submission):
                print(f"Title: {saved_item.title}")
                print(f"URL: {saved_item.url}\n")
                print(f"PERMA: {saved_item.permalink}\n")
                print(f"Subreddit: {saved_item.subreddit.display_name}\n")
            elif isinstance(saved_item, praw.models.Comment):
                print(f"Comment: {saved_item.body}")
                print(f"Link: {saved_item.link_url}\n")
                print(f"PERMA: {saved_item.permalink}\n")
                print(f"Subreddit: {saved_item.subreddit.display_name}\n")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Correct profile path - ensure it ends with the specific profile folder, not the general path
    profile_path = r"C:\Users\Daibhidh\AppData\Roaming\Mozilla\Firefox\Profiles\wpg9fojf.default-release-1662941926469"

    # Set up Firefox options to use the specified profile directly
    options = Options()
    options.add_argument(f"-profile")
    options.add_argument(profile_path)

    # Initialize the Firefox driver with the specified options
    service = FirefoxService()  # Assuming you have the appropriate geckodriver in PATH or specified

    driver = webdriver.Firefox(service=service, options=options)


    try:
        actions = ActionChains(driver)
        for saved_item in reddit.user.me().saved():
            url = f"https://new.reddit.com{saved_item.permalink}"
            print(f"Opening URL: {url}")
            driver.get(url)

            time.sleep(10)

            try:

                driver.switch_to.window(driver.current_window_handle)

                driver.maximize_window()

                # Interact with the window using pyautogui for bookmarking
                pyautogui.hotkey('ctrl', 'd')

                # Wait for a second to let the bookmark window appear
                time.sleep(1)

                # Press Enter to confirm the bookmark
                pyautogui.press('enter')

                # Wait before closing the browser to see the result
                time.sleep(5)

                # alert = driver.switch_to.alert
                # alert.accept()  # Accept or dismiss the alert

                # print("Attempting to bookmark the page...")
                #
                #
                # body = driver.find_element(By.CLASS_NAME, "grid-container")
                #
                # # actions.key_down(Keys.CONTROL).pause(1).send_keys('d').key_up(Keys.CONTROL).send_keys(Keys.RETURN).perform()
                #
                # actions.context_click(body).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.RETURN).send_keys(Keys.RETURN).perform()
                #
                # print("got here :(")
                #
                #
                # time.sleep(15)

            except Exception as e:
                print(f"Failed to click the bookmark star: {e}")
    finally:
        driver.quit()



    conn = sqlite3.connect(r"C:\Users\Daibhidh\AppData\Roaming\Mozilla\Firefox\Profiles\wpg9fojf.default-release-1662941926469\places.sqlite")
    cursor = conn.cursor()


    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    print("Tables in SQLite database:", tables)


    reddit_bookmarks_query =  f"""
    SELECT p.url, b.id
    FROM moz_bookmarks b
    JOIN moz_places p ON b.fk = p.id
    WHERE p.url LIKE '%reddit%' AND b.type = 1;
    """
    cursor.execute(reddit_bookmarks_query)
    all_reddit_bookmarks = cursor.fetchall()

        # urls.extend([url[0] for url in booked_urls])

    cleaned_reddit_bookmarks = list(set(all_reddit_bookmarks))

    bookmarks_dict = [{'url': bookmark[0], 'id': bookmark[1]} for bookmark in cleaned_reddit_bookmarks]

    count = 0

    for bookmark in bookmarks_dict:
        try:
            search_results = reddit.submission(url=bookmark['url'])
            sub_name = search_results.subreddit.display_name
            bookmark['sub'] = sub_name

            count += 1
            print(count)
        except:
            print(f"{bookmark['url']} is not available")

    print(bookmarks_dict[0])

    find_reddit_folder_query = "SELECT id FROM moz_bookmarks WHERE title = 'reddit' and type = 2";
    cursor.execute(find_reddit_folder_query)
    reddit_folder = cursor.fetchall()

    if reddit_folder:
        reddit_folder_id = reddit_folder[0][0]
    else:
        print("Reddit folder not found.")
        reddit_folder_id = None

    for bookmark in bookmarks_dict:
        try:
            sub_folder_query = f"""
                    SELECT b.id
                    FROM moz_bookmarks b
                    WHERE b.title = '{bookmark['sub']}' AND b.type = 2
                    """
            cursor.execute(sub_folder_query)
            folder_id = cursor.fetchone()

            if folder_id:
                folder_id = folder_id[0]
            else:
                folder_id = None

            if folder_id:
                update_query = f"""
                            UPDATE moz_bookmarks
                            SET parent = {folder_id}
                            WHERE id = {bookmark['id']};
                        """
                cursor.execute(update_query)
                conn.commit()
            else:

                create_folder_query = f"""
                        INSERT INTO moz_bookmarks (type, fk, parent, position, title, dateAdded, lastModified, guid, syncStatus)
                        VALUES (
                            2, 
                            NULL, 
                            {reddit_folder_id}, 
                            (SELECT IFNULL(MAX(position), 0) + 1 FROM moz_bookmarks WHERE parent = {reddit_folder_id}), 
                            '{bookmark['sub'].replace("'", "''")}', 
                            strftime('%s', 'now') * 1000000, 
                            strftime('%s', 'now') * 1000000, 
                            hex(randomblob(12)), 
                            1
                        );
                    """

                print("Executing Create Folder Query:\n", create_folder_query)  # Debugging: print the query
                cursor.execute(create_folder_query)
                conn.commit()

                # Fetch the newly created folder ID
                sub_folder_query = f"""
                        SELECT b.id
                        FROM moz_bookmarks b
                        WHERE b.title = '{bookmark['sub'].replace("'", "''")}' AND b.type = 2;
                    """
                cursor.execute(sub_folder_query)
                folder_id = cursor.fetchone()

                if folder_id:
                    folder_id = folder_id[0]
                    update_query = f"""
                            UPDATE moz_bookmarks
                            SET parent = {folder_id}
                            WHERE id = {bookmark['id']};
                            """
                    cursor.execute(update_query)
                    conn.commit()
                else:
                    print(f"Failed to create or find the folder for {bookmark['sub']}.")
        except Exception as e:
            print(f"An error occurred while updating or creating bookmarks: {e}")
    # finally:
    #     if conn:
    #         conn.close()





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