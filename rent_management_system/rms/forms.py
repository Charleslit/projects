
class PayRentForm(FlaskForm):
   tenant = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
   ammount =     StringField('Email', 
                       validators=[DataRequired(),Email()])                     
   
   submit = SubmitField('pay')
