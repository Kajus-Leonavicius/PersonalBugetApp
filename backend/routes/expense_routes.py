from flask_smorest import Blueprint, abort
from models import ExpenseModel
from schemas import ExpenseGetSchema, ExpensePostSchema, ExpensesCategory
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from helper import save_to_db
from database_conn import db 

expense_bp = Blueprint('Expenses', __name__, url_prefix = '/expenses')

@expense_bp.route('/')
class Expenses(MethodView):
    
    @expense_bp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    @expense_bp.response(200, ExpenseGetSchema(many=True))
    def get (self):
        identity = get_jwt_identity()
        
        return ExpenseModel.query.filter_by(user_id = identity).all()
    
    @expense_bp.doc(security=[{"bearerAuth": []}])
    @expense_bp.arguments(ExpensePostSchema)
    @jwt_required()
    @expense_bp.response(201, ExpenseGetSchema)
    def post (self, data): 
        
        identity = get_jwt_identity()
        
        new_expense = ExpenseModel(**data, user_id = identity)
        
        save_to_db(new_expense)
        
        return new_expense

@expense_bp.route('/<uuid:expense_id>')
class Expense(MethodView):
    
    @expense_bp.doc(security=[{"bearerAuth": []}])
    @expense_bp.arguments(ExpensePostSchema)
    @jwt_required()
    @expense_bp.response(201, ExpenseGetSchema)
    def put(self, updated_data, expense_id):
        identity = get_jwt_identity()
        
        expense = ExpenseModel.query.get_or_404(expense_id)
        
        if str(expense.user_id) != identity:
            abort(403, message = "you don't have permission edit or delete this data")
        
        for key, value in updated_data.items():
            setattr(expense, key, value)
        
        db.session.commit()
        return expense
    
    @expense_bp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    @expense_bp.response(200, ExpenseGetSchema)
    def delete(self, expense_id):
        identity = get_jwt_identity()
        expense = ExpenseModel.query.get_or_404(expense_id)
        
        if str(expense.user_id) != identity:
            abort(403, message = "you don't have permission edit or delete this data")
        
        db.session.delete(expense)
        db.session.commit()
        return expense

@expense_bp.route('/expense_type/<string:expense_type>')
class Classified(MethodView): 
    
    @expense_bp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    @expense_bp.response(200, ExpenseGetSchema(many=True))
    def get (self, expense_type):
        identity = get_jwt_identity()
        
        filtered = ExpenseModel.query.filter_by(user_id = identity, expenseType = expense_type).all()
        
        if not filtered: 
            return 'no data'
        else:
            return filtered
        
@expense_bp.route('/categories')
class Categories(MethodView): 
    
    @expense_bp.doc(security=[{"bearerAuth": []}])
    @jwt_required()
    @expense_bp.response(200, ExpensesCategory(many=True))
    def get (self):
        identity = get_jwt_identity()
        
        filtered = ExpenseModel.query.filter_by(user_id = identity).all()
        
        return filtered