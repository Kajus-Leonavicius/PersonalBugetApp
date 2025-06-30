from marshmallow import fields, Schema

class UserGetSchema(Schema):
    
    id = fields.UUID()
    email = fields.String()
    name = fields.String()
    surname = fields.String()
    created_at = fields.DateTime()
    access_token = fields.String()

class LoginResponseSchema(Schema):
    user = fields.Nested(UserGetSchema)
    access_token = fields.String()

class UserPostSchema(Schema):
    
    email = fields.String(required= True)
    password = fields.String(required= True)
    name = fields.String(required= True)
    surname = fields.String(required=True)

class UserLoginSchema(Schema):
    email = fields.String(required= True)
    password = fields.String(required= True)