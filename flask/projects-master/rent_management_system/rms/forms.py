from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField,BooleanField ,TextAreaField
from wtforms.validators import DataRequired,Length, Email ,EqualTo, ValidationError
from rms.models import User



class RegistrationForm(FlaskForm):
   username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
   email = StringField('Email', 
                       validators=[DataRequired(),Email()])
   password = PasswordField('password', validators=[DataRequired()])
   confirm_password =  PasswordField('confirm password', 
                                    validators=[DataRequired(), EqualTo('password')])
   submit = SubmitField('Signup')
   def validate_username(self , username):
      user = User.query.filter_by(username= username.data).first()
      if user:
         raise ValidationError('that username is taken. please choose another one. ')
   def validate_email(self , email):
      user = User.query.filter_by(email= email.data).first()
      if user:
         raise ValidationError('that email is taken. please choose another one. ')

   
class LoginForm(FlaskForm):
      email = StringField('email', 
                       validators=[DataRequired(),Email()])
      password= PasswordField('password', validators=[DataRequired()])
      remember=BooleanField('remember me')
      submit = SubmitField('Login') 

class UpdateAccountForm(FlaskForm):
   username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
   email = StringField('Email', 
                       validators=[DataRequired(),Email()])
   
   picture = FileField('update profile picture',validators=[FileAllowed(['jpg', 'png'])])
   submit = SubmitField('Update')
   
   def validate_username(self , username):
      if username.data != current_user.username:
       user = User.query.filter_by(username= username.data).first()
       if user:
         raise ValidationError('that username is taken. please choose another one. ')
   def validate_email(self , email):
      if email.data != current_user.email:
       user = User.query.filter_by(email= email.data).first()
       if user:
         raise ValidationError('that email is taken. please choose another one. ')
class PostForm(FlaskForm):
   title = StringField('title',
                           validators=[DataRequired()])
   content = TextAreaField('content', validators=[DataRequired()])                        
   submit = SubmitField('Post')
class RequestResetForm(FlaskForm):
   email = StringField('email', 
                       validators=[DataRequired(),Email()])
   submit = SubmitField(' request Reset')                     

   def validate_email(self , email):
      user = User.query.filter_by(email= email.data).first()
      if user is None:
         raise ValidationError('no account with that email . you mus register. ')

class ResetPasswordForm(FlaskForm):
   password = PasswordField('password', validators=[DataRequired()])
   confirm_password =  PasswordField('confirm password', 
                                    validators=[DataRequired(), EqualTo('password')])
   submit = SubmitField('reset')

class PayRentForm(FlaskForm):
   tenant = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
   ammount =     StringField('Email', 
                       validators=[DataRequired(),Email()])                     
   
   submit = SubmitField('pay')
