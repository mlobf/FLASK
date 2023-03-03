from marshmallow import Schema, fields

""" 
    Marshmellow can only check the 
    income data. So is unable to check 
    existing data. 
"""


# Item------------------------------------------------------------------------
class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)


# Store-----------------------------------------------------------------------
class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class StoreUpdateSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
