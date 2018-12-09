import logging
from datetime import datetime, timedelta

from config import CRYPTO_TIMESERIES_INDEX_NAME, DYNAMODB_TABLE_NAME
from flask_restplus import Resource
from infrastructure.dynamodb import (CryptoDynamoExpressionBuilder,
                                     QueryBuilder, execute_query)

from . import ns

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@ns.route('/data')
class MyResource(Resource):
    def get(self):

        kwargs = (
            QueryBuilder(DYNAMODB_TABLE_NAME, CRYPTO_TIMESERIES_INDEX_NAME)
            .set_batch_size_to(65)
            .with_query_expression(
                CryptoDynamoExpressionBuilder()
                .with_crypto_code("BTC")
                .since(datetime.utcnow() - timedelta(hours=24))
            )
            .build_query_kwargs()
        )
        resp = execute_query(**kwargs)
        return {
            "results": resp["Items"]
        }, 200
