class RedditUnsaveHandler:
    def __init__(self, saved_items, found_urls):
        self.saved_items = saved_items
        self.found_urls = found_urls

    def unsave_matching_items(self):
        for saved_item in self.saved_items:
            permalink = saved_item.permalink
            if any(permalink in url for url in self.found_urls):
                saved_item.unsave()
                print(f"Unsaved item: {saved_item.permalink}")