from datetime import datetime
from flask import Flask , render_template ,flash, redirect ,url_for
from forms import RegistrationForm,LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5161d89653efc3056cc624fd3aac9243'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(20),unique=True, nullable= False)
     email = db.Column(db.String(20),unique=True, nullable= False)
     image_file = db.Column(db.String(20),unique=True, nullable= False)
     password = db.Column(db.String(60), nullable= False)
     posts = db.relationship('Post',backref='author',lazy=True)
     def __repr__(self):
          return f"User('{self.username}','{self.password}','{self.image_file}')"
    
     
class Post(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       title = db.Column(db.String(100),nullable=False)
       date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
       content = db.Column(db.Text, nullable=False)
       user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
       def __rer__(self):
            return f"User('{self.title}', '{self.date_posted}')"
       

posts =[
      {'author':'jane doue',
      'date':'23/4/5',
      'title':'jany',
      'content':'first post'
},
{
      'author':'james',
      'date':'7/67/234',
      'title':'vikings',
      'content':'first post'

}

]


@app.route("/")

@app.route("/Home")
def Home():
      return render_template('Home.html', posts=posts)

@app.route('/About')
def about():
      return render_template('About.html', title='About')

@app.route('/Register',methods=['GET', 'POST'])
def register():
      form = RegistrationForm()
      if form.validate_on_submit():
           flash(f'account created for{form.username.data}!','success' )
           return redirect(url_for('Home'))
      return render_template('register.html', title='Register', form=form )
@app.route('/login', methods=['GET', 'POST'])
def login():
      form = LoginForm()
      if form.validate_on_submit():
           if form.email.data == 'admin@blog.com' and form.password.data == 'admin@12':
                flash('you have been logged in succcesfully', 'success')
                return redirect(url_for('Home'))
           else:
                flash('login unsuccesfull . please check username and password', 'danger')
      return render_template('login.html', title='Login', form= form )

      
if __name__ == '__main__':
 app.run(debug=True)