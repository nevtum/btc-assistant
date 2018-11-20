class BitcoinMarketData:
    def __init__(self, timestamp, price, volume, url):
        self.timestamp = timestamp
        self.last_price = price
        self.volume = volume
        self.url = url

    def __repr__(self):
        return "{}(timestamp={} price_btc={} volume={})".format(
            self.__class__.__name__,
            self.timestamp,
            self.last_price,
            self.volume
        )
