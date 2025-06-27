from marshmallow import fields, Schema

class ExpenseGetSchema(Schema):
    
    id = fields.UUID()
    amount = fields.Float()
    category = fields.String()
    description = fields.String()
    date = fields.DateTime()
    
class ExpensePostSchema(Schema):
    
    amount = fields.Float(required=True)
    category = fields.String(required=True)
    description = fields.String(required=True)
    date = fields.DateTime(required=True)