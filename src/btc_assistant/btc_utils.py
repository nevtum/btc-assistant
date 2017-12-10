
import json

from dateutil import parser

from .http_utils import RESTClient

root_api = "https://api.independentreserve.com"

class IndependentReserveUrls:
    @staticmethod
    def market_data_url(primary_currency_code, secondary_currency_code):
        return "{}/Public/GetMarketSummary?primaryCurrencyCode={}&secondaryCurrencyCode={}".format(
            root_api, primary_currency_code, secondary_currency_code
        )

class BTCPriceChecker:
    def get_btc_day_market_data(self, currency_code):
        if currency_code.lower() not in ['aud', 'usd']:
            raise AttributeError("Must specify either 'aud' or 'usd' currency code")
        url = IndependentReserveUrls.market_data_url('xbt', currency_code.lower())
        a_dict = RESTClient.get(url).json()
        return BTCDayMarketData(a_dict)

class BTCDayMarketData:
    def __init__(self, a_dict):
        self.data = a_dict
    
    @property
    def timestamp(self):
        return parser.parse(self.data['CreatedTimestampUtc'])

    @property
    def last_price(self):
        return self.data['LastPrice']

    @property
    def volume(self):
        return self.data['DayVolumeXbt']
    
    @property
    def raw_data(self):
        return self.data

    def __repr__(self):
        return "{}(timestamp={} price_btc={} volume={})".format(
            self.__class__.__name__,
            self.timestamp,
            self.last_price,
            self.volume
        )
