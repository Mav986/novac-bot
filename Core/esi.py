import json
import os

from esipy import EsiApp, EsiClient

from Core import _config
from Core.bot import logger

from esipy.cache import FileCache

meta_app = EsiApp()
esiapp = meta_app.get_latest_swagger

esiclient = EsiClient(
    retry_requests=True,
    cache=FileCache(path=os.path.join(os.path.dirname(__file__), '.webcache')),
    headers={'User-Agent': _config.ESI_USER_AGENT},
    raw_body_only=True
)


# TODO Log warning headers. Not sure how to access the header. Googled around a bit, but couldn't find anything solid


def get_id(name, category):
    """
    Get the id of something
    :param name: name of something
    :param category: ESI category the something is part of
    :return: either a json object containing the something id or None
    """
    if len(name) > 2:
        id_search = esiapp.op['get_search'](search=name, categories=category, strict=True)
        response = esiclient.request(id_search)
        return _check_result(response).get(category, [])

    return None


def get_ship_info(ship_name):
    """
    Get the information of a ship
    :param ship_name: ship to retreive info for
    :return: either a json object containing the ship info or None
    """
    ship_id = get_id(ship_name, 'inventory_type')
    if ship_id:
        ship_search = esiapp.op['get_universe_types_type_id'](type_id=ship_id[0])
        response = esiclient.request(ship_search)
        return _check_result(response)

    return None


def get_system_info(system_name):
    """
    Get the information of a system
    :param system_name: system to retreive info for
    :return: either a json object containing the system info or None
    """
    system_id = get_id(system_name, 'solar_system')
    if system_id:
        system_search = esiapp.op['get_universe_systems_system_id'](system_id=system_id[0])
        response = esiclient.request(system_search)
        return _check_result(response)

    return None


def search_type(name):
    """
    Search item types
    :param name: Search string
    :return: List of matching typeIDs
    """
    result = search(name, categories=('inventory_type'))

    return result.get('inventory_type', [])


def search(search, categories=('inventory_type'), strict=False):
    """
    Search EVE entities
    :param search: Term to search for
    :param categories: List of categories to check
    :param strict: Whether to use strict search.
    :return:
    """
    op = esiapp.op['get_search'](categories=categories, search=search, strict=strict)

    result = esiclient.request(op)
    return _check_result(result)

def names(type_list):
    """
    Get full name for a list of typeIDs
    :param type_list: List of valid typeIDs
    :return: List of dicts containing typeID, Name and group
    """
    op = esiapp.op['post_universe_names'](ids=type_list)

    result = esiclient.request(op)

    return _check_result(result)


def get_sell_orders(types, region_id=10000002):
    """
    Get all sell orders for list of types in a given region
    :param types: List of valid typeIDs
    :param region_id: region ID to be checked
    :return: List of dicts containing market info.
    """
    ops = [esiapp.op['get_markets_region_id_orders'](region_id=region_id, type_id=t, order_type='sell') for t in types]

    results = esiclient.multi_request(ops, threads=30)
    results_json = []
    for request, result in results:
        results_json.append(_check_result(result))
    return results_json


def _check_result(result):
    """
    Check if an ESI result is valid
    :param result: PySwagger result object from esipy
    :return: Json parsed to dict.
    """
    dictn = json.loads(result.raw.decode('utf-8'))
    if result.status == 200:
        return dictn
    else:
        logger.error("{}: {}".format(result.status, dictn.get('error')))
        raise ValueError(dictn.get('error', ''))
