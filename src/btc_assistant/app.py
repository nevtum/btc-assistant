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
        pct_change = (data.last_price / prev_data.last_price - 1) * 100

        message = self._format_message(f"{command.code}AUD", data.last_price, pct_change)
        self.presenter.display(message)

    def _handle_request_ma(self, command):
        sample_data = self.storage.get_last_records(command.total_ticks + 1)
        data = sample_data[-1]
        previous_samples = sample_data[:-1]
        if len(previous_samples) == 0:
            previous_samples = [data]
        price_data = map(lambda r: r.last_price, previous_samples)
        price_stat = MovingAverage(list(price_data), 2)
        price_stat.take_measurement(data.last_price)

        message = self._format_message(f"{command.code}AUD", price_stat.average(), price_stat.pct_change())
        self.presenter.display(message)
    
    def _format_message(self, currency_pair, price, pct_change):
        sign = "" if pct_change < 0 else "+"
        return f"{currency_pair}: ${price:.2f}, Change: ({sign}{pct_change:.3f}%)"

    def process(self, command):
        try:
            func = self.handlers[command.__class__.__name__]
            return func(command)
        except IndexError as e:
            raise IndexError("No handler found for {}".format(command.__class__.__name__))
