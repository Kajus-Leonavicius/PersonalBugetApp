from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models import SavingGoalModel
from schemas import SavingGoalGetSchema, SavingGoalPostSchema
from flask_jwt_extended import get_jwt_identity, jwt_required
from database_conn import db
from helper import save_to_db

saving_bp = Blueprint('Savings', __name__, url_prefix = '/savings')

@saving_bp.route('/')
class Savings(MethodView):
    
    @saving_bp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    @saving_bp.response(200, SavingGoalGetSchema(many= True))
    def get(self):
        identity = get_jwt_identity()
        
        return SavingGoalModel.query.filter_by(user_id = identity).all()
    
    @saving_bp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    @saving_bp.arguments(SavingGoalPostSchema)
    @saving_bp.response(201, SavingGoalGetSchema)
    def post(self, data):
        
        identity = get_jwt_identity()
        
        new_saving = SavingGoalModel(**data, user_id = identity)
        save_to_db(new_saving)
        return new_saving

@saving_bp.route('/<uuid:saving_id>')
class Saving(MethodView):
    
    @saving_bp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    @saving_bp.arguments(SavingGoalPostSchema)
    @saving_bp.response(201, SavingGoalGetSchema)
    def put(self, updated_data, saving_id):
        
        identity = get_jwt_identity()
        
        saving = SavingGoalModel.query.get_or_404(saving_id)
        
        if str(saving.user_id) != identity:
            abort(403, message = "you don't have permission edit or delete this data")
        
        for key, value in updated_data.items():
            setattr(saving, key, value)
        
        db.session.commit()
        return saving
    
    @saving_bp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    @saving_bp.response(200, SavingGoalGetSchema)
    def delete(self, saving_id):
        identity = get_jwt_identity()
        saving = SavingGoalModel.query.get_or_404(saving_id)
        
        if str(saving.user_id) != identity:
            abort(403, message = "you don't have permission edit or delete this data")
        
        db.session.delete(saving)
        db.session.commit()
        return saving