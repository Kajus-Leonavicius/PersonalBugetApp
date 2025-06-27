from flask import Flask
from flask_cors import CORS
from database_conn import db
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from dotenv import load_dotenv
import os 
from models import *
from routes import *

load_dotenv()

USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DBNAME = os.getenv('DBNAME')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)


app.config["API_TITLE"] = 'User API'
app.config["API_VERSION"] = 'v1'
app.config["OPENAPI_VERSION"] = '3.0.3'
app.config["OPENAPI_URL_PREFIX"] = '/'
app.config["OPENAPI_SWAGGER_UI_PATH"] = '/docs'
app.config["OPENAPI_SWAGGER_UI_URL"] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = 'super-slaptas-raktas'
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_size": 5,
    "max_overflow": 10,
    "pool_timeout": 30
}

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
api = Api(app)

api.spec.components.security_scheme(
    "bearerAuth",
    {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
)
api.spec.security = [{"bearerAuth": []}]

api.register_blueprint(user_bp)
api.register_blueprint(expense_bp)
api. register_blueprint(saving_bp)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug = True)