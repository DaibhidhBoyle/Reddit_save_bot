import Secrets

import praw

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options

class SetupPraw:
    def __init__(self, profile_path):
        self.profile_path = profile_path
        self.reddit = self.setupPraw()
        self.service, self.options = self.pathing()
        self.driver = self.setupDriver()
        self.saved_items = self.getSaved()

    def setupPraw(self):
        return praw.Reddit(
            client_id=Secrets.secret_info['client_id'],
            client_secret=Secrets.secret_info['client_secret'],
            username=Secrets.secret_info['username'],
            password=Secrets.secret_info['password'],
            user_agent=Secrets.secret_info['user_agent']
        )

    def pathing(self):

        options = Options()
        options.add_argument(f"-profile")
        options.add_argument(self.profile_path)

        service = FirefoxService()

        return service, options

    def setupDriver(self):

        try:
            driver = webdriver.Firefox(service=self.service, options=self.options)
            print("WebDriver initialized successfully!")
            return driver
        except Exception as e:
            print(f"Error initializing WebDriver: {e}")

    def getSaved(self):
        return list(self.reddit.user.me().saved(limit=None))