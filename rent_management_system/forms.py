from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired,Length, Email ,EqualTo




class RegistrationForm(FlaskForm):
   username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
   email = StringField('Email', 
                       validators=[DataRequired(),Email()])
   password = PasswordField('password', validators=[DataRequired()])
   confirm_password =  PasswordField('confirm password', 
                                    validators=[DataRequired(), EqualTo('password')])
   submit = SubmitField('Signup')

class LoginForm(FlaskForm):
      email = StringField('email', 
                       validators=[DataRequired(),Email()]),
      password= PasswordField('password', validators=[DataRequired()]),
      remember=BooleanField('remember me')
      submit = SubmitField('Login')