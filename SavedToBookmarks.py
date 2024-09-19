from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

import time

class SavedToBookmark:
    def __init__(self, driver):
        self.driver = driver
        self.permalinks = []
        self.actions = ActionChains(driver)

    def process_saved_items(self, saved_items):
        #build urls
        try:
            for saved_item in saved_items:
                permalink = saved_item.permalink
                self.permalinks.append(permalink)

                url = f"https://new.reddit.com{permalink}"

                self.bookmark_page(url)

        finally:
            self.driver.quit()

    def bookmark_page(self, url):
        #open urls and bookmark

        print(f"Opening URL: {url}")
        #open url in firefox
        self.driver.get(url)
        #loading time
        time.sleep(10)

        try:
            # "click" on page so follow commands affect that firefox instance
            self.driver.switch_to.window(self.driver.current_window_handle)
            self.driver.maximize_window()

            #bookmark shortcut
            pyautogui.hotkey('ctrl', 'd')
            #loading time
            time.sleep(1)
            #confirm bookmark save on menu
            pyautogui.press('enter')
            #loding time
            time.sleep(5)

        except Exception as e:
            print(f"Failed to bookmark the page: {e}")