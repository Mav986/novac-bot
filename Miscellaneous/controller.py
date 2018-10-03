from random import randint

import praw
import requests

from Miscellaneous._config import SECRET, AGENT, ID, REDDIT_WHITELIST, MAX_POSTS, MAX_INDEX

reddit = praw.Reddit(client_id=ID, client_secret=SECRET, user_agent=AGENT)


def get_xkcd_url(arg):
    """
    Get the XKCD comic URL specified by arg
    :param arg: an integer representing the comic to be retreived
    :return: string containing the xkcd url
    """
    response = requests.get('https://xkcd.com/info.0.json')
    xkcd_json = response.json()
    max_url = xkcd_json['num']
    if arg.isdigit() and 0 < int(arg) <= max_url:
        return 'https://xkcd.com/{comic_num}'.format(comic_num=arg)
    elif arg == 'random':
        return 'https://xkcd.com/{comic_num}'.format(comic_num=randint(1, max_url))
    else:
        return 'Invalid webcomic. Try again with an integer between 1 and ' + str(max_url)


def get_url_from_subreddit(subreddit_name, index):
    while True:
        subreddit = reddit.subreddit(subreddit_name)
        posts = [post for post in subreddit.new(limit=MAX_POSTS)]
        submission = posts[index % MAX_INDEX]
        index += 1
        if not submission.is_self and any(s in submission.url for s in REDDIT_WHITELIST):
            break

    return submission.url
