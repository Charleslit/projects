from flask_wtf import FlaskForm
from  wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
class PayRentForm(FlaskForm):
   name = StringField('name',
                           validators=[DataRequired(), Length(min=2, max=20)])
   amount = StringField('amount', 
                       validators=[DataRequired()])                     
   
   submit = SubmitField('pay')

class RentForm(FlaskForm):
   name = StringField('name',
                           validators=[DataRequired(), Length(min=2, max=20)])
   amount = StringField('amount', 
                       validators=[DataRequired()])                     
   
   submit = SubmitField('pay')