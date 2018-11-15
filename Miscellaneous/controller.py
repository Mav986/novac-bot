import random
import requests
from Miscellaneous._config import DOOSTER_PHRASES


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
        return 'https://xkcd.com/{comic_num}'.format(comic_num=random.randint(1, max_url))
    else:
        return 'Invalid webcomic. Try again with an integer between 1 and ' + str(max_url)


def get_dustey_phrase():
    return random.choice(DOOSTER_PHRASES)
