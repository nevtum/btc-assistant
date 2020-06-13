root_api = "https://api.independentreserve.com"

class IndependentReserveUrls:
    @staticmethod
    def market_data_url(primary_currency_code, secondary_currency_code):
        return "{}/Public/GetMarketSummary?primaryCurrencyCode={}&secondaryCurrencyCode={}".format(
            root_api, primary_currency_code, secondary_currency_code
        )