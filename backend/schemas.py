from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Integer(required=False)
    title = fields.String(required=True)
    description = fields.String(required=False)
    due_date = fields.String(required=False)
    completed = fields.Boolean(required=False)