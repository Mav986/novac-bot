from datetime import datetime
from random import randint
from Core import esi
import requests


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


def get_server_status(datasource='tranquility'):
    """Generate a reply describing the status of an EVE server/datasource."""

    response = esi.get_status(datasource)
    server_name = datasource.capitalize()

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