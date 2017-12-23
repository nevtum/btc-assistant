import logging
import time

from btc_assistant.btc_utils import BTCPriceChecker
from btc_assistant.storage import PickleStorage
from btc_assistant.sql_storage import create_database_storage
from btc_assistant.stats import MovingAverage

logging.basicConfig(level=logging.INFO)

def create_price_checker():
    return BTCPriceChecker()

MAX_RECORDS = 10

def do_check():
    checker = create_price_checker()
    storage = create_database_storage()
    sample_data = storage.get_last_records(MAX_RECORDS)
    sample_data = map(lambda r: r.last_price, sample_data)
    price_stat = MovingAverage(list(sample_data), MAX_RECORDS)
    data = checker.get_btc_day_market_data('AUD')
    storage.store_record(data)
    price_stat.take_measurement(data.last_price)
    print("timestamp: %s" % data.timestamp.strftime('%d, %b %Y - %H:%M:%S'))
    print("%i minute average price: %.2f" % (len(price_stat), price_stat.average()))
    print("pct changed: {:.3f}%".format(price_stat.pct_change()))
    print("std-dev: %.2f" % price_stat.std_deviation())
    print("current price: %.2f" % data.last_price)
    print()

def main():
    while True:
        do_check()
        time.sleep(60)

if __name__ == '__main__':
    main()
