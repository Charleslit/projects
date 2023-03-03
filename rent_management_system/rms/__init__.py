import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from rms.config import Config
  
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category ='info'
mail = Mail(app)

from rms.rent.routes import rent
from rms.users.routes import users
from rms.posts.routes import posts
from rms.main.routes import main
app.register_blueprint(rent)
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)