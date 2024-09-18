from urllib.parse import quote

class RedditUnsaver:
    def __init__(self, saved_items, found_urls):
        self.saved_items = saved_items
        self.found_urls = found_urls

    def unsave_matching_items(self):

        for url in self.found_urls:
            print("poop train" + " " + url)


        for saved_item in self.saved_items:

            permalink = saved_item.permalink

            decoded_permalink = quote(permalink, safe=':/')

            if any(decoded_permalink in url for url in self.found_urls):

                saved_item.unsave()
                print(f"Unsaved item: {saved_item.permalink}")
