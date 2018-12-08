import time

import factory
from infrastructure.network import BTCPriceChecker

MAX_RECORDS = 10

def write_btc_data():
    checker = factory.create_price_checker()
    storage = factory.create_storage()
    data = checker.get_btc_day_market_data('AUD')
    storage.store_record(data)

def main():
    from analysis import RequestPriceMovingAverage
    command = RequestPriceMovingAverage("BTC", "m", 10)
    assistant = factory.create_btc_assistant()

    while True:
        write_btc_data()
        assistant.process(command)
        time.sleep(60)

def main2():
    from infrastructure.dynamodb import DynamoDB
    storage = DynamoDB('crypto-market-data')
    for data in storage.enumerate_records("BTC"):
        print(data)

if __name__ == '__main__':
    main2()
