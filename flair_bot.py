"""Flair bot."""
import sys
import os
import re
import codecs
import csv
from time import gmtime, strftime
import praw

config = {
    "app": {
        "app_id":     os.environ.get("app_app_id"),
        "app_secret": os.environ.get("app_app_secret"),
        "user_agent": "WhoWouldWin Bot by /u/TheD3xus",
        "auth_type":  "script"
    },
    "auth-script": {
        "username": os.environ.get("reddit_username", None),
        "password": os.environ.get("reddit_password", None),
    },
    "auth-webapp": {
        "token": os.environ.get("auth_webapp_token", None)
    },
    "logging": {
        "logging": True
    },
    "subject": {
        "subject": "flair"
    },
    "subreddit": {
        "name": "WhoWouldWin"
    }
}

class FlairBot:
    """Flair bot."""

    def __init__(self):
        """Initial setup."""

        self.flairs = {}
        self.reddit = None

        os.chdir(sys.path[0])

        self.logging = config["logging"]["logging"]

        self.login()

    def login(self):
        """Log in via script/web app."""

        app_id = config["app"]["app_id"]
        app_secret = config["app"]["app_secret"]
        user_agent = config["app"]["user_agent"]

        if config["app"]["auth_type"] == 'webapp':
            token = config["auth-webapp"]["token"]
            self.reddit = praw.Reddit(client_id=app_id,
                                        client_secret=app_secret,
                                        refresh_token=token,
                                        user_agent=user_agent)
        else:
            username = config["auth-script"]["username"]
            password = config["auth-script"]["password"]
            self.reddit = praw.Reddit(client_id=app_id,
                                        client_secret=app_secret,
                                        username=username,
                                        password=password,
                                        user_agent=user_agent)

        self.get_flairs()

    def get_flairs(self):
        """Read flairs from CSV."""

        with open('flair_list.csv') as csvf:
            csvf = csv.reader(csvf)
            flairs = {}
            for row in csvf:
                if len(row) == 2:
                    flairs[row[0]] = row[1]
                else:
                    flairs[row[0]] = None

        self.flairs = flairs
        self.fetch_pms()

    def fetch_pms(self):
        """Grab unread PMs."""

        target_sub = config["subreddit"]["name"]
        valid = r'[A-Za-z0-9_-]+'
        subject = config["subject"]["subject"]
        unreadPMs = self.reddit.inbox.unread()
        if len(unreadPMs) > 0:
            print("New PMs to process, starting...")
            for msg in self.reddit.inbox.unread():
                author = str(msg.author)
                valid_user = re.match(valid, author)
                if msg.subject == subject and valid_user:
                    self.process_pm(msg, author, target_sub)
        else:
            print("No new PMs to process, exiting...")
        sys.exit()

    def process_pm(self, msg, author, target_sub):
        """Process unread PM."""

        content = msg.body.split(',', 1)
        class_name = content[0].rstrip()
        subreddit = self.reddit.subreddit(target_sub)

        if class_name in self.flairs:
            if len(content) > 1:
                flair_text = content[1].lstrip()[:64]
            else:
                flair_text = self.flairs[class_name] or ''

            subreddit.flair.set(author, flair_text, class_name)
            if self.logging:
                self.log(author, flair_text, class_name)

        msg.mark_read()

    @staticmethod
    def log(user, text, cls):
        """Log applied flairs to file."""

        with codecs.open('log.txt', 'a', 'utf-8') as logfile:
            time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            log = 'user: ' + user
            log += ' | class(es): ' + cls
            if len(text):
                log += ' | text: ' + text
            log += ' @ ' + time_now + '\n'
            logfile.write(log)
