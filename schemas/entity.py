from marshmallow import Schema, fields


class CreateEntitySchema(Schema):
  type = fields.Str(required=True)
  name = fields.Str(required=True)
  minPrice = fields.Number(required=True)
  maxPrice = fields.Number(required=True)
