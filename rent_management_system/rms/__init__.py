import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
  
app = Flask(__name__)
app.config['SECRET_KEY'] = '5161d89653efc3056cc624fd3aac9243'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rocket.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category ='info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USERNAME']= os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD']= os.environ.get('EMAIL_PASS')
mail = Mail(app)


from rms.users.routes  import users 
from rms.posts.routes  import posts 
from rms.main.routes  import main 

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)