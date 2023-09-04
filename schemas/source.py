from marshmallow import Schema, fields


class SourceSchema(Schema):
  name = fields.Str(required=True)
