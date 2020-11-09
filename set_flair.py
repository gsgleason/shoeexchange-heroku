import threading
import praw

def set_gyw_score(user):

    reddit = praw.Reddit()

    comment_score = 0
    post_score = 0
    
    for comment in reddit.redditor(user).comments.new(limit=None):
        if comment.subreddit.display_name == 'goodyearwelt':
            comment_score += comment.score
    for submission in reddit.redditor(user).submissions.new(limit=None):
        if submission.subreddit.display_name == 'goodyearwelt':
            post_score += submission.score
    
    score = post_score + comment_score
    reddit.subreddit('Shoeexchange').flair.set(user, 'GYW Score: {} '.format(score))

users_to_check = []

reddit = praw.Reddit()

for comment in reddit.subreddit('Shoeexchange').comments(limit=None):
    if comment.author is None:
        continue
    if comment.author == "AutoModerator":
        continue
    user = comment.author.name
    if user in users_to_check:
        continue
    users_to_check.append(user)

for user in users_to_check:
    t = threading.Thread(target=set_gyw_score, args=(user,))
    t.start()
                
