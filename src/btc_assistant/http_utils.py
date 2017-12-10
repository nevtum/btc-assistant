import logging

import requests
from urllib3.exceptions import HTTPError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RESTClient:
    @classmethod
    def get(cls, url):
        headers = {
            'Content-Type': 'application/json',
        }
        res = requests.get(url, headers=headers)
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
        res = requests.post(url, json=a_dict, headers=headers)
        if not res.ok:
            raise HTTPError("url={} status_code={} text={}".format(
                    res.status_code,
                    res.text
                )
            )
        return res