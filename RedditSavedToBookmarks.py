import Secrets

from Praw import SetupPraw
from BookMarkSQL import SetupBookmarkSQL
from SavedToBookmarks import SavedToBookmark
from CheckBookmark import CheckBookmark
from Unsave import RedditUnsaver
from GetUnsortedBookMarks import GetUnsortedBookmarks
from SortBookmarks import RedditBookmarkManager

class RedditSavedToBookmarks:
    def __init__(self):

        self.db_path = Secrets.db

    def run(self):

        print( self.db_path)
        #Connect to reddit and grab all the saved posts connected to the user
        praw = SetupPraw(self.db_path)
        #sets up:
        #reddit
        #driver
        #saved_items

        #Connect to the Firfox Database for Bookmarks and Places
        bookmarkSQL = SetupBookmarkSQL(self.db_path+"\places.sqlite")
        # conn -- firefox bookmarks
        # cursor -- firefox bookmarks

        #Move the Saved Reddit Post into Bookmarks (using browser puppetering not SQL)
        save_to_bookmarks = SavedToBookmark(praw.driver)
        #permalink
        save_to_bookmarks.process_saved_items(praw.saved_items)

        #Double check that the Saved Reddit Post made it to the Bookmarks and return only a list of those that did
        check_if_saved_is_in_checkBookmark = CheckBookmark()
        new_urls_in_bookmark = check_if_saved_is_in_checkBookmark.find_matching_urls(save_to_bookmarks.permalinks, bookmarkSQL.cursor)

        #take all reddit post that made it to the bookmarks and unsave them
        unsaver = RedditUnsaver(praw.saved_items, new_urls_in_bookmark)
        unsaver.unsave_matching_items()

        #returning the id of the folder where the reddit saved post were placed then returns
        unsorted_bookmarks = GetUnsortedBookmarks(bookmarkSQL.conn, bookmarkSQL.cursor)
        new_bookmarks_folder = unsorted_bookmarks.getMostRecentEntryParent()

        if(new_bookmarks_folder):
            # find all the unsorted reddit bookmarks that were just added
            bookmark_dict = unsorted_bookmarks.fetch_reddit_bookmarks(new_bookmarks_folder)

            sort_bookmarks = RedditBookmarkManager(bookmarkSQL.conn, bookmarkSQL.cursor, praw.reddit)
            #put each new reddit bookmark into a folder with it's appropriate sub name; if it does not exist then create one
            sort_bookmarks.fetch_subreddit_for_bookmarks(bookmark_dict)
            sort_bookmarks.organise_bookmarks()

        bookmarkSQL.close_connection()






