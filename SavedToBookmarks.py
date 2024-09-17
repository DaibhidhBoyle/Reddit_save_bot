import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options

class SavedToBookmark:
    def __init__(self, driver, saved_items):
        self.driver = driver
        self.saved_items = saved_items
        self.permalinks = []
        self.actions = ActionChains(driver)

    def process_saved_items(self):
        try:
            for saved_item in self.saved_items:
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
            # Make sure the current window is active
            self.driver.switch_to.window(self.driver.current_window_handle)
            self.driver.maximize_window()

            # Use pyautogui to trigger the bookmark hotkey
            pyautogui.hotkey('ctrl', 'd')
            time.sleep(1)  # Let the bookmark window appear
            pyautogui.press('enter')
            time.sleep(5)  # Give time for the action to complete

        except Exception as e:
            print(f"Failed to bookmark the page: {e}")