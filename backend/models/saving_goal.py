from database_conn import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class SavingGoalModel(db.Model):
    __tablename__ = 'saving_goal'
    
    id = db.Column(UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable = False)
    name = db.Column(db.String(255))
    target = db.Column(db.Float)
    target_date = db.Column(db.DateTime)
    started_date = db.Column(db.DateTime, default = datetime.utcnow)
    current_saved = db.Column(db.Float)