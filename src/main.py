import logging
import time

from btc_assistant.btc_utils import BTCPriceChecker
from btc_assistant.storage import PickleStorage
from btc_assistant.sql_storage import create_database_storage

logging.basicConfig(level=logging.INFO)

def create_data_storage():
    import os
    filename = 'btc_data.pickle'
    filepath = os.path.join(os.path.dirname(__file__), '..', filename)
    return PickleStorage(filepath)

def create_price_checker():
    return BTCPriceChecker()

def main():
    checker = create_price_checker()
    storage = create_database_storage()
    while True:
        data = checker.get_btc_day_market_data('AUD')
        storage.store_record(data)
        time.sleep(60)

if __name__ == '__main__':
    main()
