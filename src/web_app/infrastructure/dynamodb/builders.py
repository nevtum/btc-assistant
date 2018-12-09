class CryptoDynamoExpressionBuilder:
    def __init__(self):
        self.start_datetime = None
        self.end_datetime = None

    def with_crypto_code(self, currency_code):
        self.currency_code = currency_code
        return self

    def since(self, start_datetime):
        self.start_datetime = start_datetime
        return self

    def until(self, end_datetime):
        self.end_datetime = end_datetime
        return self

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
        query_exp = {
            ":sym": {
                "S": self.currency_code,
            }
        }
        if self.start_datetime:
            query_exp[":t1"] = { "S": self.start_datetime.isoformat() }
        if self.end_datetime:
            query_exp[":t2"] = { "S": self.end_datetime.isoformat() }
        return query_exp

    def as_dict(self):
        return {
            "KeyConditionExpression": self._build_key_condition_expression(),
            "ExpressionAttributeValues": self._build_expression_attributes(),
        }

class QueryBuilder:
    def __init__(self, table_name, index_name=None):
        self.table_name = table_name
        self.index_name = index_name
        self.item_limit = 500
    
    def set_batch_size_to(self, batch_size):
        self.item_limit = batch_size
        return self

    def with_query_expression(self, expression_builder):
        self.expression_builder = expression_builder
        return self

    def build_query_kwargs(self):
        args = {
            "TableName": self.table_name,
            "Limit": self.item_limit,
            **self.expression_builder.as_dict()
        }
        if self.index_name:
            args["IndexName"] = self.index_name
            args["ReturnConsumedCapacity"] = "INDEXES"
        else:
            args["ReturnConsumedCapacity"] = "TOTAL"
        return args
