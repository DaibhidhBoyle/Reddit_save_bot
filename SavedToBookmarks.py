from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

import time

class SavedToBookmark:
    def __init__(self, driver):
        self.driver = driver
        self.permalinks = []
        self.actions = ActionChains(driver)

    def process_saved_items(self, saved_items):
        try:
            for saved_item in saved_items:
                permalink = saved_item.permalink
                self.permalinks.append(permalink)

                url = f"https://new.reddit.com{permalink}"

                self.bookmark_page(url)

        finally:
            self.driver.quit()

    def bookmark_page(self, url):

        print(f"Opening URL: {url}")
        self.driver.get(url)
        time.sleep(10)

        try:

            self.driver.switch_to.window(self.driver.current_window_handle)
            self.driver.maximize_window()


            pyautogui.hotkey('ctrl', 'd')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(5)

        except Exception as e:
            print(f"Failed to bookmark the page: {e}")