import praw
import os

def get_reddit():
    return praw.Reddit(
            user_agent=os.environ.get("PRAW_USER_AGENT"),
            client_id=os.environ.get("PRAW_CLIENT_ID"),
            client_secret=os.environ.get("PRAW_CLIENT_SECRET"),
            username=os.environ.get("PRAW_USERNAME"),
            password=os.environ.get("PRAW_PASSWORD")
            )
