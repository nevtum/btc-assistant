import logging
from datetime import datetime

from factory import create_market_data_gateway
from flask_restplus import Resource

from . import ns

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

gw = create_market_data_gateway()

@ns.route("/data/<float:unix_timestamp>")
@ns.doc(params={'unix_timestamp': '86400.0'})
class BitcoinMarketList(Resource):
    def get(self, unix_timestamp):
        dt_ref = datetime.fromtimestamp(unix_timestamp)
        resp = gw.get_bitcoin_market_data(dt_ref)
        return {
            "count": len(resp["Items"]),
            "next_page_url": None,
            "results": resp["Items"]
        }, 200
