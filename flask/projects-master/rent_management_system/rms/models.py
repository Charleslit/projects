from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from rms  import db,login_manager, app 
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
      return User.query.get(int(user_id))


class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(20),unique=True, nullable= False)
     email = db.Column(db.String(20),unique=True, nullable= False)
     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
     password = db.Column(db.String(60), nullable= False)
     posts = db.relationship('Post',backref='author',lazy=True)
     
     
     def get_reset_token(self, expires_sec=1800):
          s = Serializer(app.config['SECRET_KEY'])
          return s.dumps({'user_id': self.id}).encode('utf-8')
     @staticmethod
     def verify_reset_token(token):
          s = Serializer(app.config['SECRET_KEY'])
          try:
               user_id = s.loads(token)['user_id']
          except:
                    return None
          return User.query.get(user_id)

def __repr__(self):
          return f"User('{self.username}','{self.password}', '{self.image_file}')"
     
class Post(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       title = db.Column(db.String(100),nullable=False)
       date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
       content = db.Column(db.Text, nullable=False)
       user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
       def __repr__(self):
            return f"User('{self.title}', '{self.date_posted}')"
       
class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rent_payments = db.relationship('RentPayment', backref='tenant', lazy=True)

class RentPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)

       
