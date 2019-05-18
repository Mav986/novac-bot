from datetime import datetime

import discord

from Core import esi
import random
import requests
from Miscellaneous.config import DOOSTER_PHRASES, JUMP_MASS_CATEGORIES, DESTINATION_CATEGORIES, COLOR
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


def _running_for(start_time):
    running_for = int((datetime.utcnow() - start_time).total_seconds())
    if running_for < 60:
        return "less than a minute"

    running_for_list = []
    units = [
        (running_for // (60 * 60), "hour"),
        ((running_for // 60) % 60, "minute"),
    ]
    for number, unit in units:
        running_for_list.append("{} {}{}".format(
            number,
            unit,
            "s" * (number != 1)
        ))
    return ", ".join(running_for_list)


def get_server_status(datasource='tranquility'):
    """Generate a discord embed describing the status of an EVE server/datasource."""

    response = esi.get_status(datasource)
    server_name = datasource.capitalize()

    if response == "offline" or response == "indeterminate":

        attachment = discord.Embed(
            title="{}: {}".format(server_name, response.capitalize()),
            color=COLOR.RED,
        ).add_field(
            name="Server time",
            value=datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
        )

    else:
        vip = response.get("vip")
        started = datetime.strptime(response["start_time"], "%Y-%m-%dT%H:%M:%SZ")

        attachment = discord.Embed(
            title="{}: Online".format(server_name),
            color=COLOR.ORANGE if vip else COLOR.GREEN,
        ).add_field(
            name="Server time",
            value=datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"),
            inline=False
        ).add_field(
            name="Players online",
            value="{:,}".format(response["players"]),
            inline=False
        ).add_field(
            name="Started at",
            value=datetime.strftime(started, "%Y-%m-%d %H:%M:%S"),
            inline=False
        ).add_field(
            name="Running for",
            value=_running_for(started),
            inline=False
        )

        if vip:
            attachment.title = "{}: In VIP mode".format(server_name)

    return attachment