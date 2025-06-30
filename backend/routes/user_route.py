from flask_smorest import Blueprint
from helper import save_to_db
from models import UserModel
from schemas import UserGetSchema, UserPostSchema, LoginResponseSchema, UserLoginSchema
from flask.views import MethodView
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

user_bp = Blueprint('User', __name__, url_prefix = '/user')

@user_bp.route('/auth/register')
class Register(MethodView):
    
    @user_bp.arguments(UserPostSchema)
    @user_bp.response(201, UserGetSchema)
    def post(self, data):
        password = data.pop('password')
        hashed_password = generate_password_hash(password)
        new_user = UserModel(**data, password = hashed_password)
        
        save_to_db(new_user)
        
        return new_user

@user_bp.route('/auth/login')
class login (MethodView):
    
    @user_bp.arguments(UserLoginSchema)
    @user_bp.response(201, LoginResponseSchema)
    def post (self, data):
        email = data['email']
        password = data.pop('password')
        user = UserModel.query.filter_by(email = email).first_or_404()
        
        if user and check_password_hash(user.password, password):
            
            access_token = create_access_token(identity=str(user.id))   
        
            return {'user': user, 'access_token': access_token}