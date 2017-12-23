import logging
import time

from btc_assistant.btc_utils import BTCPriceChecker
from btc_assistant.storage import PickleStorage
from btc_assistant.sql_storage import create_database_storage
from btc_assistant.stats import StatisticalMeasure

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
    stat = StatisticalMeasure()
    checker = create_price_checker()
    storage = create_database_storage()
    sample_data = storage.get_last_records(MAX_RECORDS)
    sample_data = list(map(lambda r: r.last_price, sample_data))

    while True:
        data = checker.get_btc_day_market_data('AUD')
        storage.store_record(data)
        sample_data.append(data.last_price)
        if len(sample_data) > MAX_RECORDS:
            sample_data.pop(0)
        print("timestamp: %s" % data.timestamp)
        print("%i minute average price: %f" % (len(sample_data), stat.average(sample_data)))
        print("std-dev: %f" % stat.std_deviation(sample_data))
        print("current price: %f" % data.last_price)
        time.sleep(60)

if __name__ == '__main__':
    main()
