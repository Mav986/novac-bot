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
        response = search(name, category, True)
        return response.get(category, [])[0]

    return None


def find_type(name):
    """
    Get type info by name from ESI
    :param name: type to retreive info for
    :return: either a json object containing the type info or None
    """
    type_id = get_id(name, 'inventory_type')
    if type_id:
        return get_type(type_id)

    return None


def get_type(type_id):
    """
    Get type info by ID from ESI
    :param type_id: EVE type ID
    :return: either a json object containing the type info or None
    """
    op = esiapp.op['get_universe_types_type_id'](type_id=type_id)
    response = esiclient.request(op)
    return _check_result(response)


def get_system_info(system_name):
    """
    Get the information of a system
    :param system_name: system to retreive info for
    :return: either a json object containing the system info or None
    """
    system_id = get_id(system_name, 'solar_system')
    if system_id:
        op = esiapp.op['get_universe_systems_system_id'](system_id=system_id)
        response = esiclient.request(op)
        return _check_result(response)

    return None


def search_type(name, strict=False):
    """
    Search item types
    :param name: Search string
    :return: List of matching typeIDs
    """
    result = search(name, categories='inventory_type', strict=strict)

    return result.get('inventory_type', [])


def search(search, categories='inventory_type', strict=False):
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


def get_status(datasource='tranquility'):
    op = esiapp.op['get_status'](datasource=datasource)

    result = esiclient.request(op)

    if result.status == 200:
        return json.loads(result.raw.decode('utf-8'))
    elif result.status == 503:
        return "offline"
    else:
        return "indeterminate"


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
