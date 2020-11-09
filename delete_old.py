from datetime import datetime
import praw
import os

if os.environ.get('LISTING_MAX_AGE'):
    max_age = int(os.environ.get('LISTING_MAX_AGE'))
else:
    max_age = 90


reddit = praw.Reddit()

submissions_to_remove = []
for submission in reddit.subreddit('shoeexchange').new(limit=None):
    if submission.stickied or submission.distinguished:
        continue
    created_utc = datetime.utcfromtimestamp(submission.created_utc)
    submission_age = datetime.utcnow() - created_utc
    if submission_age.days > 90:
        submissions_to_remove.append(submission)

for submission in submissions_to_remove:
    submission.mod.remove()
    submission.mod.send_removal_message("Your listing has been expired and has been removed.  You may re-list your item if needed.")
