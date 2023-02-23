import os 
import secrets
from PIL import Image
from flask import  render_template ,flash, redirect ,url_for, request
from rms import app, db ,bcrypt
from rms.forms import RegistrationForm,LoginForm,UpdateAccountForm, PostForm
from rms.models import User, Post
from flask_login import login_user, current_user,logout_user,login_required




@app.route("/")

@app.route("/Home")
def Home():
      posts = Post.query.all()
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
def save_picture(form_picture):
      random_hex = secrets.token_hex(8)
      _, f_ext = os.path.splitext(form_picture.filename)
      picture_fn = random_hex + f_ext
      picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
      
      output_size = (125, 125)
      i = Image.open(form_picture)
      i.thumbnail(output_size)
      i.save(picture_path)

      return picture_fn

@app.route('/account' ,methods=['GET','POST'])
@login_required
def account():
      form = UpdateAccountForm()
      if form.validate_on_submit():
            if form.picture.data:
                  picture_file = save_picture(form.picture.data)
                  current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('your account has been updated succesfully ', 'success')
            return redirect(url_for('account'))
            
      elif request.method == 'GET':
                  form.username.data = current_user.username
                  form.email.data = current_user.email
      image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
      return render_template('account.html', title='account',image_file=image_file ,
                                        form=form, users=users) 
@app.route('/users')
@login_required
def users():
       users =  User.query.all()
       return render_template('users.html', title='users', users=users) 

@app.route('/post/new' ,methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
      post = Post(title= form.title.data, content = form.content.data, author = current_user)
      db.session.add(post)
      db.session.commit()

      flash('your post has been created', 'success')
      return redirect(url_for('Home'))
    return render_template('posts.html', title='newpost' , form = form ) 
    
@app.route('/post/<int:post_id>')
def post(post_id):
        posts = Post.query.get_or_404(post_id)
        return render_template('post.html',title=posts.title,posts=posts )


   