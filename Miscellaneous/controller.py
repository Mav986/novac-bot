from datetime import datetime
from Core import esi
import random
import requests
from Miscellaneous.config import DOOSTER_PHRASES, JUMP_MASS_CATEGORIES
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
        return 'https://xkcd.com/{comic_num}'.format(comic_num=random.randint(1, max_url))
    else:
        return 'Invalid webcomic. Try again with an integer between 1 and ' + str(max_url)


def get_dustey_phrase():
    return random.choice(DOOSTER_PHRASES)


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
    """Generate a reply describing the status of an EVE server/datasource."""

    response = esi.get_status(datasource)
    server_name = datasource.capitalize()

    if response == "offline":
        attachment = {
            "color": "danger",
            "title": "{} status".format(server_name),
            "text": "Offline",
            "fields": [
                {
                    "title": "Server time",
                    "value": datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"),
                    "short": True,
                },
            ],
            "fallback": "{} status: Offline".format(server_name)
        }
    elif response == "indeterminate":
        indeterminate = "Cannot determine server status. It might be offline, or experiencing connectivity issues."
        attachment = {
            "color": "danger",
            "title": "{} status".format(server_name),
            "text": indeterminate,
            "fields": [
                {
                    "title": "Server time",
                    "value": datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"),
                    "short": True,
                },
            ],
            "fallback": "{} status: {}".format(server_name, indeterminate)
        }
    else:
        vip = response.get("vip")
        started = datetime.strptime(response["start_time"], "%Y-%m-%dT%H:%M:%SZ")
        attachment = {
            "color": "warning" if vip else "good",
            "title": "{} status".format(server_name),
            "fields": [
                {
                    "title": "Players online",
                    "value": "{:,}".format(response["players"]),
                    "short": True
                },
                {
                    "title": "Server time",
                    "value": datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"),
                    "short": True,
                },
                {
                    "title": "Started at",
                    "value": datetime.strftime(started, "%Y-%m-%d %H:%M:%S"),
                    "short": True,
                },
                {
                    "title": "Running for",
                    "value": _running_for(started),
                    "short": True,
                },
            ],
            "fallback": "{} status: {:,} online, started at {}{}".format(
                server_name,
                response["players"],
                datetime.strftime(started, "%Y-%m-%d %H:%M:%S"),
                ", in VIP" * int(vip is True),
            ),
        }
        if vip:
            attachment["fields"].insert(0, {"title": "In VIP mode"})

    return attachment