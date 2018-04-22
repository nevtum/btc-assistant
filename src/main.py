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

def read_statistics():
    import pdb; pdb.set_trace()
    storage = factory.create_storage()
    sample_data = storage.get_last_records(MAX_RECORDS + 1)
    data = sample_data[-1]
    price_data = map(lambda r: r.last_price, sample_data[:-1])
    price_stat = MovingAverage(list(price_data), MAX_RECORDS)
    price_stat.take_measurement(data.last_price)
    print(data.timestamp.strftime('%d, %b %Y - %H:%M:%S'))
    print("*" * 50)
    print("current price: %.2f" % data.last_price)
    print("current volume: %.2f" % data.volume)
    print("%i minute average price: %.2f" % (len(price_stat), price_stat.average()))
    print("std-dev: %.2f" % price_stat.std_deviation())
    print("pct changed: {:.3f}%".format(price_stat.pct_change()))
    print()

def main():
    while True:
        write_btc_data()
        read_statistics()
        time.sleep(60)

if __name__ == '__main__':
    main()
