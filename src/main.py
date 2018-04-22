import time

from btc_assistant.btc_utils import BTCPriceChecker
from btc_assistant.stats import MovingAverage
import factory

MAX_RECORDS = 10

def write_btc_data():
    checker = factory.create_price_checker()
    storage = factory.create_storage()
    data = checker.get_btc_day_market_data('AUD')
    storage.store_record(data)

def main():
    from btc_assistant.commands import RequestPriceMovingAverage
    command = RequestPriceMovingAverage("BTC", "m", 10)
    assistant = factory.create_btc_assistant()

    while True:
        write_btc_data()
        assistant.process(command)
        time.sleep(60)

if __name__ == '__main__':
    main()
