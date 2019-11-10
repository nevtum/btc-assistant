import logging
from datetime import datetime

from factory import create_market_data_gateway

from . import router

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

gw = create_market_data_gateway()


@router.get("/data/{unix_timestamp}")
def get_btc_market_list(unix_timestamp: float):
    max_batch_size = 65
    dt_ref = datetime.fromtimestamp(unix_timestamp)
    resp = gw.get_bitcoin_market_data(dt_ref, max_batch_size)

    count = len(resp)
    next_page_url = None
    if count >= max_batch_size:
        next_page_ref = resp[-1].utc_timestamp.timestamp()
        next_page_url = router.url_path_for("get_btc_market_list", unix_timestamp=next_page_ref)

    data = map(lambda item: item.as_dict(), resp)
    return {"count": count, "next_page_url": next_page_url, "results": list(data)}, 200
