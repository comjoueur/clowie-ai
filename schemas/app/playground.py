from marshmallow import Schema, fields


class PlaygroundSchema(Schema):
  budgetPerDinner = fields.Number()
  preferredType = fields.List(fields.Str())
  userSuggestion = fields.Str()
  startTime = fields.Date()
  numberOfDays = fields.Number()
  meals = fields.List(fields.Str())
  esPrompt = fields.Str()
  openaiPrompt = fields.Str()
