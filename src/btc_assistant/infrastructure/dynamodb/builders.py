from datetime import datetime


class CryptoDynamoQueryBuilder:
    def __init__(self, table_name):
        self.table_name = table_name
        self.item_limit = 500
        self.start_datetime = None
        self.end_datetime = None

    def set_batch_size_to(self, batch_size):
        self.item_limit = batch_size
        return self

    def since(self, start_datetime):
        self.start_datetime = start_datetime
        return self

    def until(self, end_datetime):
        self.end_datetime = end_datetime
        return self

    def with_crypto_code(self, currency_code):
        self.currency_code = currency_code
        return self

    def build_query_kwargs(self):
        args = {
            "TableName": self.table_name,
            "IndexName": "crypto-timestamp-index",
            "Limit": self.item_limit,
            "ReturnConsumedCapacity": "INDEXES",
            "KeyConditionExpression": self._build_key_condition_expression(),
            "ExpressionAttributeValues": self._build_expression_attributes(),
        }
        return args

    def _build_key_condition_expression(self):
        base_query = "currency_code = :sym"
        if self.start_datetime and self.end_datetime:
            return f"{base_query} AND utc_timestamp BETWEEN :t1 AND :t2"
        elif self.start_datetime and not self.end_datetime:
            return f"{base_query} AND utc_timestamp >= :t1"
        elif not self.start_datetime and self.end_datetime:
            return f"{base_query} AND utc_timestamp <= :t2"
        return base_query

    def _build_expression_attributes(self):
        query_exp = {":sym": {"S": self.currency_code,}}
        if self.start_datetime:
            query_exp[":t1"] = {"S": self.start_datetime.isoformat()}
        if self.end_datetime:
            query_exp[":t2"] = {"S": self.end_datetime.isoformat()}
        return query_exp
