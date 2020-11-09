import re
import time
from db import DB
import praw
from datetime import datetime

reddit = praw.Reddit()

db = DB("submission_id", "listings")

def find_details(submission):
    for comment in submission.comments:
        if comment.is_submitter and comment.body.strip().startswith('[DETAILS]') or comment.body.strip().startswith('\[DETAILS\]') or comment.body.strip().startswith('DETAILS'):
            return comment
    return

def add_listing(comment):
    submission = comment.submission
    listing = {}
    listing['submission_id'] = submission.id
    listing['title'] = submission.title
    listing['permalink'] = submission.permalink
    listing['flair_text'] = submission.link_flair_text
    listing['url'] = submission.url
    listing['redditor'] = submission.author.name
    listing['created_utc'] = datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M')
    listing['updated_utc'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
    if submission.thumbnail.startswith('https:'):
        listing['thumbnail_url'] = submission.thumbnail
    for line in comment.body.splitlines():
        m1 = p1.search(line)
        m2 = p2.search(line)
        m3 = p3.search(line)
        m4 = p4.search(line)
        m5 = p5.search(line)
        m6 = p6.search(line)
        m7 = p7.search(line)
        m8 = p8.search(line)
        m9 = p9.search(line)
        m10 = p10.search(line)
        m11 = p11.search(line)
        m12 = p12.search(line)
        if m1:
            listing['brand'] = m1.group(1).strip('*').strip()
        if m2:
            listing['model'] = m2.group(1).strip('*').strip()
        if m3:
            listing['size'] = m3.group(1).strip('*').strip()
        if m4:
            listing['width'] = m4.group(1).strip('*').strip()
        if m5:
            listing['last'] = m5.group(1).strip('*').strip()
        if m6:
            listing['upper'] = m6.group(1).strip('*').strip()
        if m7:
            listing['sole'] = m7.group(1).strip('*').strip()
        if m8:
            listing['condition'] = m8.group(1).strip('*').strip()
        if m9:
            listing['images'] = m9.group(1).strip('*').strip()
        if m10:
            listing['notes'] = m10.group(1).strip('*').strip()
        if m11:
            listing['price'] = m11.group(1).strip('*').strip()
        if m12:
            listing['country'] = m12.group(1).strip('*').strip()
    if not listing.get('size') or not listing.get('brand') or not listing.get('price'):
        return
    db.add(listing)
    return True

body = """**Details needed**

Hi.  I'm trying to parse your post, but I'm not finding what I need.  Please make sure you have a top-level comment with an appropriately formatted list of details.  Please see [the wiki](/r/Shoeexchange/wiki/post_details) for instructions.

Failure to do so will result in your post not being added to my [listing index](https://shoeexchange.pythonanywhere.com).

Once you create or edit your top-level details comment, it should be added within 24 hours."""

p1 = re.compile('Brand:(.*)')
p2 = re.compile('Model:(.*)')
p3 = re.compile('Size:(.*)')
p4 = re.compile('Width:(.*)')
p5 = re.compile('Last:(.*)')
p6 = re.compile('Upper:(.*)')
p7 = re.compile('Sole:(.*)')
p8 = re.compile('Condition:(.*)')
p9 = re.compile('Images:(.*)')
p10 = re.compile('Notes:(.*)')
p11 = re.compile('Price:(.*)')
p12 = re.compile('Country:(.*)')

bad_posts = []
good_posts = []
i = 0
for submission in reddit.subreddit('shoeexchange').new(limit=None):
    if submission.link_flair_text == 'SOLD':
        continue
    if not submission.title.startswith(('[WTS]','[WTT]')):
        continue
    i+=1
    details = find_details(submission)
    if details:
        result = add_listing(details)
        if result:
            good_posts.append(submission)
            continue
    # if we get here then there is no details comment
    bad_posts.append(submission)

def get_bot_nag(submission):
    for comment in submission.comments:
        if not comment.author:
            continue
        if comment.author.name == 'ShoeExchangeBot' and comment.body.startswith('**Details needed**'):
            return comment
    return

# iterate over submissions missing proper detail comment and comment that I wasn't able to parse it
for submission in bad_posts:
    # check to see if bot has already commented, and if not, do so.
    if not get_bot_nag(submission):
        submission.reply(body).mod.distinguish()

# iterate over submissions that have proper detail comment and remove previous bot mod comment if it exists
for submission in good_posts:
    # remove previous nag
    nag = get_bot_nag(submission)
    if nag:
        nag.delete()
    
