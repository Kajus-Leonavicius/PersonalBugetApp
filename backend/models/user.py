from database_conn import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    email = db.Column(db.String(255))
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default = datetime.utcnow)