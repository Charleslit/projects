from datetime import datetime, timedelta

from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from rms import db, login_manager, app 
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    rent_payments = db.relationship('RentPayment', backref='tenant', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        serializer = Serializer(app.config['SECRET_KEY'])
        return serializer.dumps({'user_id': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expires_sec)})

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
            user_id = data['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_total_rent_paid(self):
        """Return the total amount of rent paid by the user."""
        total = 0
        for payment in self.rent_payments:
            total += payment.amount
        return total

    def get_rent_balance(self, rent_amount):
        """Return the balance of rent owed by the user."""
        total_paid = self.get_total_rent_paid()
        balance = rent_amount - 5000
        return balance
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
class Post(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100), nullable=False)
     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
     content = db.Column(db.Text, nullable=False)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
     
     def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
     # assume `user` is a `User` object
     

class RentPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"RentPayment('{self.amount}', '{self.name}', '{self.date}')"
