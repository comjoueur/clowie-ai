from marshmallow import Schema, fields


class CreateEntitySchema(Schema):
  name = fields.Str(required=True)
  minPrice = fields.Number(required=True)
  maxPrice = fields.Number(required=True)
