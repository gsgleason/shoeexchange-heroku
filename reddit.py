import praw
from config import config

def get_reddit():
    return praw.Reddit(
            user_agent=config['praw']['user_agent'],
            client_id=config['praw']['client_id'],
            client_secret=config['praw']['client_secret'],
            username=config['praw']['username'],
            password=config['praw']['password']
            )
