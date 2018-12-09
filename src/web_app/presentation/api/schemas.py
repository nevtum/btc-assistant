from marshmallow import Schema, fields

class BitcoinPriceSchema(Schema):
    utc_timestamp = fields.DateTime(required=True)
    value = fields.Float(required=True)
    volume = fields.Float(required=True)