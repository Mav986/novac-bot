import random
import requests
from Miscellaneous.config import DOOSTER_PHRASES, JUMP_MASS_CATEGORIES, DESTINATION_CATEGORIES
from Miscellaneous.wormhole_data import WORMHOLE_IDS
from Core.esi import get_type


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


def _get_dogma_value(wh_data, key):
    """
    Find a dictionary identified by a key, in a list of dictionaries
    :param wh_data: the dictionary to search
    :param key: the key to identify the correct dictionary
    :return: the value in the correct dictionary
    """
    dogma_attr = wh_data.get('dogma_attributes')
    return next(element for element in dogma_attr if element.get('attribute_id') == key).get('value')


def get_wormhole_stats(id):
    """
    Get attributes of a wormhole
    :param id: 4 character wormhole id
    :return: dict containing the relevant wormhole attributes
    """
    for wormhole in WORMHOLE_IDS:
        if id in wormhole.get('name'):
            wh_data = get_type(wormhole.get('id'))

            leads_to = _get_dogma_value(wh_data, 1381)
            lifetime = _get_dogma_value(wh_data, 1382)
            total_mass = _get_dogma_value(wh_data, 1383)
            regen_mass = _get_dogma_value(wh_data, 1384)
            jump_mass = _get_dogma_value(wh_data, 1385)

            return {'leads_to': DESTINATION_CATEGORIES.get(leads_to),
                    'lifetime': int(lifetime / 60),
                    'total_mass': int(total_mass),
                    'regen_mass': int(regen_mass),
                    'jump_mass': JUMP_MASS_CATEGORIES.get(jump_mass)}
