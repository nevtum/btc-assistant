import logging
from datetime import datetime, timedelta

from factory import create_market_data_gateway
from flask_restplus import Resource

from . import ns

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

gw = create_market_data_gateway()

@ns.route('/data')
class BitcoinMarketList(Resource):
    def get(self):
        resp = gw.get_bitcoin_market_data(datetime.utcnow() - timedelta(hours=24))
        return {
            "results": resp["Items"]
        }, 200
