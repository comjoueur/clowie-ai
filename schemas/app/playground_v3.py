from marshmallow import Schema, fields


class PlaygroundSchemaV3(Schema):
  budgetPerDinner = fields.Number()
  userSuggestion = fields.Str()
  startTime = fields.Date()
  numberOfDays = fields.Number()
  meals = fields.List(fields.Str())
