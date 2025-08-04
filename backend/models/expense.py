from database_conn import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class ExpenseModel(db.Model):
    __tablename__ = 'expense'
    
    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable= False)
    amount = db.Column(db.Float)
    expenseType = db.Column(db.String(255))
    category = db.Column(db.String(255))
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime, default = datetime.utcnow)
