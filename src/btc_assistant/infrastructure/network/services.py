import json

from dateutil import parser
from log import get_logger

from .http_utils import RESTClient
from .responses import BitcoinMarketData
from .urls import IndependentReserveUrls

logger = get_logger(__name__)

class BTCPriceChecker:
    def get_btc_day_market_data(self, currency_code):
        logger.debug("Getting BTC market data from Independent Reserve...")
        if currency_code.lower() not in ['aud', 'usd']:
            raise AttributeError("Must specify either 'aud' or 'usd' currency code")
        url = IndependentReserveUrls.market_data_url('xbt', currency_code.lower())
        a_dict = RESTClient.get(url).json()
        logger.info("Data retrieved: {}".format(a_dict))
        return BitcoinMarketData(
            timestamp=parser.parse(a_dict['CreatedTimestampUtc']),
            price=a_dict['LastPrice'],
            volume=a_dict['DayVolumeXbt'],
            url="www.independentreserve.com"
        )
