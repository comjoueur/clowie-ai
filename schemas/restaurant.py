from marshmallow import Schema, fields


class CreateRestaurantSchema(Schema):
  name = fields.Str(required=True)
  minPrice = fields.Number(required=True)
  maxPrice = fields.Number(required=True)
  meals = fields.List(fields.Str())
  weekdays = fields.List(fields.Str())

  description = fields.Str(optional=True)
  address = fields.Str(optional=True)
  typeOfFood = fields.Str(optional=True)
  typeOfPlace = fields.Str(optional=True)
