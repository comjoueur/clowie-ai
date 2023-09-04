from marshmallow import Schema, fields


class CreateEntityEntrySchema(Schema):
  source_id = fields.Str(required=True)

  description = fields.Str(optional=True)
  address = fields.Str(optional=True)
  typeOfFood = fields.Str(optional=True)
  rating = fields.Number(optional=True)
