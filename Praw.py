import Secrets

import praw

from selenium import webdriver

from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options

class PrawHandler:
    def __init__(self):
        self.reddit = self.setupPraw()
        self.driver = self.setupDriver(*self.pathing())
        self.saved_items = self.getSaved(reddit)

    def setupPraw(self):
        return praw.Reddit(
            client_id=Secrets.secret_info['client_id'],
            client_secret=Secrets.secret_info['client_secret'],
            username=Secrets.secret_info['username'],
            password=Secrets.secret_info['password'],
            user_agent=Secrets.secret_info['user_agent']
        )

    def pathing(self):
        profile_path = r"C:\Users\Daibhidh\AppData\Roaming\Mozilla\Firefox\Profiles\wpg9fojf.default-release-1662941926469"

        options = Options()
        options.add_argument(f"-profile")
        options.add_argument(profile_path)

        service = FirefoxService()

        return profile_path, options, service

    def setupDriver(self, profile_path, options, service):
        return webdriver.Firefox(service=service, options=options)

    def getSaved(self, reddit):
        return list(reddit.user.me().saved(limit=None))