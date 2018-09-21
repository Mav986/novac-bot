from math import sqrt

from Core.esi import find_type, get_system_info
from Navigation.config import METERS_TO_LIGHT_YEARS, JUMPDRIVE, SUBCAP


def get_dotlan_map(args):
    """
    Get a dotlan URL for the specific ship, system, and jdc level. Faster, but requires strict ordering of parameters.
    :param args: a list of strings containing the ship name, system name, and jdc level
    :return: a dotlan URL
    """
    jdc = _set_jdc(args[1])
    system_info = get_system_info(args[0])
    ship_info = find_type(args[2])
    if system_info and ship_info:
        return _create_dotlan_url(ship_info, system_info, jdc)

    return None


def get_jump_dist(arg):
    """
    Get the direct LY distance between 2 systems. Does not calculate LY traveled when using mids.
    :param arg: List of 2 systems to calculate the distance between
    :return: Distance between 2 systems
    """
    system_one = get_system_info(arg[0])
    system_two = get_system_info(arg[1])
    if system_two and system_one:
        return _get_distance(system_one, system_two)

    return None


def _get_distance(system_one, system_two):
    """
    Get coordinates of 2 systems and calculate their distance in light years
    :param system_one:
    :param system_two:
    :return: distance between 2 systems
    """
    x1, y1, z1 = _get_coordinates(system_one)
    x2, y2, z2 = _get_coordinates(system_two)
    distance_in_meters = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    distance = float(distance_in_meters * METERS_TO_LIGHT_YEARS)

    return distance


def _get_coordinates(system_info):
    """
    Get the coordinates of a system
    :param system_info:
    :return: a list containing the xyz coordinates of a system
    """
    x = system_info['position']['x']
    y = system_info['position']['y']
    z = system_info['position']['z']

    return x, y, z


def _create_dotlan_url(ship_info, system_info, jdc):
    """
    Craft a dotlan jump planner url using the provided parameters
    :param ship_info: json object containing all the ship info
    :param system_info: json object containing all the system info
    :param jdc: integer representing the jdc level
    :return: a dotlan url
    """
    jump_capable = _jump_capable(ship_info)
    if jump_capable:
        return JUMPDRIVE.format(ship=ship_info['name'], jdc=jdc, system=system_info['name'])
    else:
        return SUBCAP.format(jdc=jdc, system=system_info['name'])


def _jump_capable(ship_info):
    """
    Determine whether the ship is a jump drive capable ship. Note: attribute 869 is 'jump drive spool time'.
    All jump drive capable ships have this attribute to the best of my knowledge.
    :param ship_info: json object containing all the ship info
    :return: a boolean on whether or not the ship is jump drive capable
    """
    for attribute in ship_info['dogma_attributes']:
        if attribute['attribute_id'] == 869:
            return True

    return False


def _set_jdc(jdc):
    """
    Validate the jdc level
    :param jdc: a string representing the jdc level
    :return: an integer representing the jdc level
    """
    try:
        if 1 <= int(jdc) <= 5:
            return jdc
        else:  # if jdc is int but out of range
            raise ValueError
    except ValueError:
        return 5
