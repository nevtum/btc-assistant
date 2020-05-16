from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class BitcoinMarketData:
    timestamp: datetime
    price: Decimal
    volume: Decimal
    url: str
    symbol: str
