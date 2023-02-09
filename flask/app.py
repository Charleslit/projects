from flask import Flask , render_template, session , redirect, url_for
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField ,SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)

moment = Moment(app)
form = Form

class NameForm(form):
    name= StringField('what is your name ' ,validators=[DataRequired()])
    submit=SubmitField('submit')

app.config['SECRET_KEY'] = 'hard to guess string'
@app.route('/')
def index():
 return render_template('index.html')
@app.route('/reg/', methods=['GET', 'POST'])
def user(name):
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
    return render_template('user.html', form=form, name=name)
@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html',current_time=datetime.utcnow()), 404
@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500e.html'),500
if __name__ == '__main__':
 app.run(debug=True)