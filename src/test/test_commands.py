import unittest

from btc_assistant.app import (BTCAssistant, RequestCurrentPrice,
                               RequestPriceMovingAverage)
from btc_assistant.storage import StorageBase


def parse_input(text):
    if text == "BTC price":
        return RequestCurrentPrice("BTC")
    elif text == "BTC ma 10m":
        return RequestPriceMovingAverage("BTC", "m", 10)

class InMemoryStorage(StorageBase):
    def __init__(self, records):
        self.records = records

    def get_last_records(self, num_records):
        return self.records[-num_records:]

    def store_record(self, record):
        self.records.append(record)

class PriceRecord:
    def __init__(self, price):
        self.last_price = price
    
    def __repr__(self):
        return "{}(price={})".format(self.__class__.__name__, self.last_price)

class MockPresenter:
    def __init__(self):
        self.output = ""
    
    def display(self, text):
        self.output = text

class TestCommands(unittest.TestCase):
    def setUp(self):
        records = [
            PriceRecord(18166.50),
            PriceRecord(10146.92),
            PriceRecord(15322.00),
            PriceRecord(17729.95),
            PriceRecord(13567.18),
            PriceRecord(18113.63),
            PriceRecord(18113.63),
            PriceRecord(18166.50),
            PriceRecord(17451.80),
            PriceRecord(17574.00),
        ]
        self.storage = InMemoryStorage(records)
        self.presenter = MockPresenter()
        self.assistant = BTCAssistant(self.storage, self.presenter)

    def test_get_btc_market_price_command(self):
        command = parse_input("BTC price")
        self.assistant.process(command)
        self.assertEqual(self.presenter.output, "BTCAUD: $17574.00, Change: (+0.350%)")
    
    def test_get_btc_market_price_command_10min_moving_average(self):
        command = parse_input("BTC ma 10m")
        self.assistant.process(command)
        self.assertEqual(self.presenter.output, "BTCAUD: $16242.85, Change: (-0.404%)")

    @unittest.SkipTest
    def test_submit_price_notification(self):
        self.fail("Not implemented")
    
    @unittest.SkipTest
    def test_list_active_notifications(self):
        self.fail("Not implemented")
    
    @unittest.SkipTest
    def test_request_btc_balance(self):
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
