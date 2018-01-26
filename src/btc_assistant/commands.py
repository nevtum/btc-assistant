class RequestCurrentPrice:
    def __init__(self, crypto_code):
        self.code = crypto_code

class RequestPriceMovingAverage:
    def __init__(self, crypto_code, scale, nr_ticks):
        self._validate_scale(scale)
        self.code = crypto_code
        self.scale = scale
        self.nr_ticks = nr_ticks
        self._map = {
            "m": 1,
            "H": 60,
            "D": 3600
        }
    
    def _validate_scale(self, scale):
        assert(scale in ["m", "H", "D"])
    
    @property
    def total_ticks(self):
        return self._map[self.scale] * self.nr_ticks