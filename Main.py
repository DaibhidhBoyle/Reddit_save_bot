# main.py
import praw
import Secrets

def main():
    # Set up Reddit client with credentials from Secrets.py
    reddit = praw.Reddit(
        client_id=Secrets.secret_info['client_id'],
        client_secret=Secrets.secret_info['client_secret'],
        username=Secrets.secret_info['username'],
        password=Secrets.secret_info['password'],
        user_agent=Secrets.secret_info['user_agent']
    )

    # Fetch and print saved items (posts and comments)
    try:
        for saved_item in reddit.user.me().saved(limit=2):
            if isinstance(saved_item, praw.models.Submission):
                print(f"Title: {saved_item.title}")
                print(f"URL: {saved_item.url}\n")
                print(f"Subreddit: {saved_item.subreddit.display_name}\n")
            elif isinstance(saved_item, praw.models.Comment):
                print(f"Comment: {saved_item.body}")
                print(f"Link: {saved_item.link_url}\n")
                print(f"Subreddit: {saved_item.subreddit.display_name}\n")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()