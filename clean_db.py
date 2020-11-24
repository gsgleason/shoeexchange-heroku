from db import DB
import praw

reddit = praw.Reddit()

db = DB("submission_id", "listings")

for listing in db.fetchall():
    s = reddit.submission(id=listing['submission_id'])
    if s.removed_by_category:
        db.delete(listing['submission_id'])
    if s.link_flair_text == 'SOLD':
        db.delete(listing['submission_id'])
