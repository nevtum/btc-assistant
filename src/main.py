import logging
import time

from btc_assistant.btc_utils import BTCPriceChecker
from btc_assistant.storage import PickleStorage
from btc_assistant.sql_storage import create_database_storage
from btc_assistant.stats import MovingAverage

logging.basicConfig(level=logging.INFO)

def create_data_storage():
    import os
    filename = 'btc_data.pickle'
    filepath = os.path.join(os.path.dirname(__file__), '..', filename)
    return PickleStorage(filepath)

def create_price_checker():
    return BTCPriceChecker()

MAX_RECORDS = 10

def main():
    checker = create_price_checker()
    storage = create_database_storage()
    sample_data = storage.get_last_records(MAX_RECORDS)
    sample_data = map(lambda r: r.last_price, sample_data)
    stat2 = MovingAverage(list(sample_data), MAX_RECORDS)

    while True:
        data = checker.get_btc_day_market_data('AUD')
        storage.store_record(data)
        stat2.take_measurement(data.last_price)
        print("timestamp: %s" % data.timestamp)
        print("%i minute average price: %.2f" % (len(stat2), stat2.average()))
        print("pct changed: {:.2f}%".format(stat2.pct_change()))
        print("std-dev: %.2f" % stat2.std_deviation())
        print("current price: %.2f" % data.last_price)
        print()
        time.sleep(60)

if __name__ == '__main__':
    main()
