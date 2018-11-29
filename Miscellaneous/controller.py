from random import randint
import requests
from Miscellaneous.config import JUMP_MASS_CATEGORIES
from Miscellaneous.wormhole_data import WORMHOLE_IDS


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


def _get_jumpable_mass(jump_mass):
    """
    Get a string representing the jumpable mass of a wormhole
    :param jump_mass: a comma-separated string representing an integer (eg. 1,000,000)
    :return: a short string representation of the jumpable mass
    """
    mass = jump_mass.replace(',', '')
    return JUMP_MASS_CATEGORIES.get(int(mass))


def get_wormhole_stats(id):
    """
    Get attributes of a wormhole
    :param id: 4 character wormhole id
    :return: dict containing the relevant wormhole attributes
    """
    if id in WORMHOLE_IDS:
        wh = WORMHOLE_IDS[id]
        jumpable_mass = _get_jumpable_mass(wh["jumpMass"])
        wh_info = {
            "leadsTo": wh["leadsTo"],
            "jumpMass": jumpable_mass,
            "totalMass": wh["totalMass"],
            "maxLifetime": str(wh["maxLifetime"])
        }

        return wh_info
