# Tool imports
import os
import praw
import sys

# Function imports
from update_stylesheet import update_stylesheet

reddit = praw.Reddit(
    client_id=os.environ.get("app_app_id"),
    client_secret=os.environ.get("app_app_secret"),
    password=os.environ.get("reddit_password", None),
    refreshtoken=os.environ.get("auth_webapp_token", None),
    user_agent='testscript by /u/fakebot3',
    username=os.environ.get("reddit_username", None)
)

subreddit = reddit.subreddit("whowouldmod")

# Command line argument parsing

curArg = sys.argv[1:]

if curArg[0] == "--stylesheet":
    update_stylesheet(subreddit)

