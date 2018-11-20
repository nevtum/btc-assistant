import json

from dateutil import parser

from .http_utils import RESTClient
from .log import get_logger
from .responses import BitcoinMarketData

logger = get_logger(__name__)

root_api = "https://api.independentreserve.com"

class IndependentReserveUrls:
    @staticmethod
    def market_data_url(primary_currency_code, secondary_currency_code):
        return "{}/Public/GetMarketSummary?primaryCurrencyCode={}&secondaryCurrencyCode={}".format(
            root_api, primary_currency_code, secondary_currency_code
        )

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