import logging
from datetime import datetime

from factory import create_market_data_gateway
from flask import url_for
from flask_restplus import Resource

from . import ns
from .schemas import BitcoinPriceSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

gw = create_market_data_gateway()

@ns.route("/data/<float:unix_timestamp>")
@ns.doc(params={'unix_timestamp': '86400.0'})
class BitcoinMarketList(Resource):
    def get(self, unix_timestamp):
        max_batch_size = 65
        dt_ref = datetime.fromtimestamp(unix_timestamp)
        resp = gw.get_bitcoin_market_data(dt_ref, max_batch_size)

        schema = BitcoinPriceSchema(many=True)
        results = schema.dump(resp)
        if results.errors:
            return results.errors, 500

        data = results.data
        count = len(data)

        next_page_url = None
        if count >= max_batch_size:
            assert(len(resp) == count)
            next_page_ref = resp[-1].utc_timestamp.timestamp()
            next_page_url = url_for("api.market_bitcoin_market_list", unix_timestamp=next_page_ref)

        return {
            "count": count,
            "next_page_url": next_page_url,
            "results": data
        }, 200
