from marshmallow import fields, Schema

class ExpenseGetSchema(Schema):
    
    id = fields.UUID()
    amount = fields.Float()
    category = fields.String()
    description = fields.String()
    date = fields.DateTime()
    expenseType= fields.String()
    
class ExpensePostSchema(Schema):
    
    amount = fields.Float(required=True)
    category = fields.String(required=True)
    description = fields.String(required=True)
    expenseType= fields.String(required = True)
    
class ExpensesCategory(Schema):
    amount = fields.String()
    category = fields.String()