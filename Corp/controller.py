import requests
from Corp._config import SRP_URL, SRP_URL_WITH_COMMENT
from Corp.config import LOSS_FORMAT
from Core.esi import get_id


def submit_srp(name, url, extra=None):
    if extra:
        extra = extra.strip()
        requests.post(SRP_URL_WITH_COMMENT.format(name=name, killmail_url=url, extra_info=extra))
    else:
        requests.post(SRP_URL.format(name=name, killmail_url=url))


def valid_lossmail(url):
    request = requests.get(url)
    if LOSS_FORMAT in url and request.status_code == 200:
        return True
    else:
        return False


def valid_character(name):
    try:
        get_id(name, 'character')
        return True
    except IndexError:
        return False
