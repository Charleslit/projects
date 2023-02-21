from flask import  render_template ,flash, redirect ,url_for, request
from rms import app, db ,bcrypt
from rms.forms import RegistrationForm,LoginForm
from rms.models import User, Post
from flask_login import login_user, current_user,logout_user,login_required

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
      if current_user.is_authenticated:
            return redirect(url_for('Home'))
      form = RegistrationForm()
      if form.validate_on_submit():
           hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf_8')
           user = User(username = form.username.data, email = form.email.data, password = hashed_password )
           db.session.add(user)
           db.session.commit()
           flash(f'account created for{form.username.data}!','success' )
           return redirect(url_for('Home'))
      return render_template('register.html', title='Register', form=form )
@app.route('/login', methods=['GET', 'POST'])
def login():
      if current_user.is_authenticated:
            return redirect(url_for('Home'))
      form = LoginForm()
      if form.validate_on_submit():
           user = User.query.filter_by(email= form.email.data).first()
           if user and bcrypt.check_password_hash(user.password, form.password.data):
               login_user(user,remember=form.remember.data)
               next_page = request.args.get('next')
               flash('you have been logged in succcesfully', 'success')
               return redirect(url_for('Home'))
           else:
                flash('login unsuccesfull . please check username and password', 'danger')
      return render_template('login.html', title='Login', form= form )

@app.route('/logout')
def logout():
      logout_user()
      return redirect(url_for('Home'))

@app.route('/account')
@login_required
def account():
      image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
      return render_template('account.html', title='account',image_file=image_file ) 
