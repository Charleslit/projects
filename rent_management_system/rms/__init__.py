from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
  
app = Flask(__name__)
app.config['SECRET_KEY'] = '5161d89653efc3056cc624fd3aac9243'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rocket.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category ='info'

from rms import routes 