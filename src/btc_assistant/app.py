from .commands import RequestCurrentPrice, RequestPriceMovingAverage
from .stats import MovingAverage

class BTCAssistant:
    def __init__(self, storage, presenter):
        self.storage = storage
        self.presenter = presenter
        self._setup_handlers()
    
    def _setup_handlers(self):
        self.handlers = {}
        self.handlers[RequestCurrentPrice.__name__] = self._handle_request_current_price
        self.handlers[RequestPriceMovingAverage.__name__] = self._handle_request_ma
    
    def _handle_request_current_price(self, command):
        sample_data = self.storage.get_last_records(2)
        assert(len(sample_data) > 0)
        data = sample_data[-1]
        prev_data = sample_data[-2]
        change = (data.last_price / prev_data.last_price - 1) * 100

        sign = "+"
        if change < 0:
            sign = ""
        message = "{}AUD: ${:.2f}, Change: ({}{:.3f}%)".format(
            command.code, data.last_price, sign, change
        )
        self.presenter.display(message)

    def _handle_request_ma(self, command):
        sample_data = self.storage.get_last_records(command.total_ticks + 1)
        data = sample_data[-1]
        price_data = map(lambda r: r.last_price, sample_data[:-1])
        price_stat = MovingAverage(list(price_data), 2)
        price_stat.take_measurement(data.last_price)

        sign = "+"
        if price_stat.pct_change() < 0:
            sign = ""
        message = "{}AUD: ${:.2f}, Change: ({}{:.3f}%)".format(
            command.code, price_stat.average(), sign, price_stat.pct_change()
        )
        self.presenter.display(message)

    def process(self, command):
        try:
            func = self.handlers[command.__class__.__name__]
        except IndexError as e:
            raise IndexError("No handler found for {}".format(command.__class__.__name__))
        func(command)
