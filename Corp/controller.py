import requests
from Corp._config import SRP_URL, SRP_URL_WITH_COMMENT, LOSS_FORMAT


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
