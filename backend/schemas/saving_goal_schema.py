from marshmallow import Schema, fields

class SavingGoalGetSchema(Schema):
    
    id = fields.UUID()
    name = fields.String()
    target = fields.Float()
    target_date = fields.DateTime()
    started_date = fields.DateTime()
    current_saved = fields.Float()
    
class SavingGoalPostSchema(Schema):
    
    name = fields.String(required= True)
    name = fields.String(required= True)
    target = fields.Float(required= True)
    target_date = fields.DateTime(required= True)
    current_saved = fields.Float(required= True)