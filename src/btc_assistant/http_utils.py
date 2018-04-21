import logging

import requests
from urllib3.exceptions import HTTPError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RESTClient:
    default_timeout = 10

    @classmethod
    def get(cls, url):
        headers = {
            'Content-Type': 'application/json',
        }
        res = requests.get(url, headers=headers, timeout=RESTClient.default_timeout)
        if not res.ok:
            raise HTTPError("url={} status_code={} text={}".format(
                    url,
                    res.status_code,
                    res.text
                )
            )
        return res

    @classmethod
    def post(cls, url, a_dict):
        headers = {
            'Content-Type': 'application/json',
        }
        res = requests.post(url, json=a_dict, headers=headers, timeout=RESTClient.default_timeout)
        if not res.ok:
            raise HTTPError("url={} status_code={} text={}".format(
                    res.status_code,
                    res.text
                )
            )
        return res