import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

from Fleetup.fleetup_config import FU_APP_URI, FU_GROUP_ID

session = requests.session()
cached_session = CacheControl(session, cache=FileCache('.webcache'))


# TODO Test/fix lockfile permissions error
def get_doctrines():
    """
    Fetch list of all doctrines from fleetup.
    :return: Dictionary containing all doctrine names and IDs.
    """
    uri = '/'.join((FU_APP_URI, 'Doctrines', FU_GROUP_ID))
    json = get_json(uri)

    if json and 'Data' in json:
        data = json['Data']
        names = {d['Name']: d['DoctrineId'] for d in data}
        return names


def get_fittings(doctrine=None):
    """
    Get list of fittings, optionally filtered by doctrine if a name is passed and can be conclusively matched.
    :param doctrine: Partial or full doctrine name.
    :return: Tuple of a message and a Dictionary of doctrine names and IDs.
    """
    if not doctrine:
        return get_all_fittings()
    else:
        doctrines = get_doctrines()
        doctrine_id = doctrines.get(doctrine, False)
        # TODO: Refactor search, currently all over the place.
        filtered = [d for d in doctrines.keys() if all(w in d.lower() for w in doctrine.lower().split())]
        if not doctrine_id and len(filtered) == 1:
            doctrine_id = doctrines.get(filtered[0])
        if not doctrine_id:
            return "Doctrine {} not found. Partial matches:\n{}".format(doctrine, '\n'.join(filtered) or None), {}
        else:
            return 'Fittings for doctrine *{}*:'.format(filtered[0]), get_doctrine_fittings(doctrine_id)


def get_all_fittings():
    """
    Fetch list of all fittings from fleetup
    :return: Dictionary containing all fitting names and ids.
    """
    uri = '/'.join((FU_APP_URI, 'Fittings', FU_GROUP_ID))
    json = get_json(uri)

    if json and 'Data' in json:
        data = json['Data']
        names = {d['Name']: d['FittingId'] for d in data}
        return names


def get_doctrine_fittings(doctrine_id):
    """
    Get fittings for a specific doctrine
    :param doctrine_id: Doctrine ID to fetch
    :return: Dictionary containing doctrine fitting names and ids
    """
    uri = '/'.join((FU_APP_URI, 'DoctrineFittings', str(doctrine_id)))
    json = get_json(uri)

    if json and 'Data' in json:
        data = json['Data']
        names = {d['Name']: d['FittingId'] for d in data}
        return names


def get_fitting(name):
    """
    Get a single fitting by name. Returns fitting list if no conclusive match is found.
    :param name: Full or partial fitting name
    :return: EFT formatted fitting or error message.
    """
    fittings = get_fittings()
    fitting_id = fittings.get(name, False)
    filtered = [f for f in fittings.keys() if all(w in f.lower() for w in name.lower().split())]
    if len(filtered) == 1 and not fitting_id:
        fitting_id = fittings.get(filtered[0])
    if not fitting_id:
        return "*Fitting {} not found.* Partial matches:\n{}".format(name, '\n'.join(filtered) or 'None')
    else:
        return '```{}```'.format(get_eft_fit(fitting_id))


def get_eft_fit(fitting_id):
    """
    Get a fitting in EFT format from fleetup.
    :param fitting_id: Fitting ID to be fetched
    :return: Fitting in EFT format or "Not found"
    """
    uri = '/'.join((FU_APP_URI, 'Fitting', str(fitting_id), 'eft'))
    json = get_json(uri)

    if json and 'Data' in json:
        return json['Data']['FittingData']
    else:
        return "Not found"


def get_json(uri):
    """
    Get json result from an uri. Hits cache if applicable.
    :param uri: URI to be called
    :return: Json parsed as dict.
    """
    res = cached_session.get(uri)

    if res.status_code == 200:
        return res.json()
    else:
        # TODO: Handle HTTP Errors
        return None
