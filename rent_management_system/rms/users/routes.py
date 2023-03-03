from flask import Blueprint , render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from rms import db , bcrypt
from rms.models import User, Post, RentPayment
from rms.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from rms.users.utils import save_picture , send_reset_email
from datetime import datetime 

users = Blueprint('users', __name__)

@users.route('/Register',methods=['GET', 'POST'])
def register():
      if current_user.is_authenticated:
            return redirect(url_for('main.Home'))
      form = RegistrationForm()
      if form.validate_on_submit():
           hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf_8')
           user = User(username = form.username.data, email = form.email.data, password = hashed_password )
           db.session.add(user)
           db.session.commit()
           flash(f'account created for{form.username.data}!','success' )
           return redirect(url_for('main.Home'))
      return render_template('register.html', title='Register', form=form )
@users.route('/login', methods=['GET', 'POST'])
def login():
      if current_user.is_authenticated:
            return redirect(url_for('main.Home'))
      form = LoginForm()
      if form.validate_on_submit():
           user = User.query.filter_by(email= form.email.data).first()
           if user and bcrypt.check_password_hash(user.password, form.password.data):
               login_user(user,remember=form.remember.data)
               next_page = request.args.get('next')
               flash('you have been logged in succcesfully', 'success')
               return redirect(url_for('main.Home'))
           else:
                flash('login unsuccesfull . please check username and password', 'danger')
      return render_template('login.html', title='Login', form= form )

@users.route('/logout')
def logout():
      logout_user()
      return redirect(url_for('main.Home'))

@users.route('/account' ,methods=['GET','POST'])
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
            return redirect(url_for('users.account'))
            
      elif request.method == 'GET':
                  form.username.data = current_user.username
                  form.email.data = current_user.email
      image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
      return render_template('account.html', title='account',image_file=image_file ,
                                        form=form, users=users) 


@users.route('/user/<username>')
def user_posts(username):

      page = request.args.get('page',1, type= int)
      user = User.query.filter_by(username= username).first_or_404()
      posts = Post.query.filter_by(author = user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page = page ,per_page=5)
      return render_template('user_posts.html', posts=posts ,user=user ) 

@users.route('/reset_password' ,methods=['GET','POST'])
def reset_request():
      if current_user.is_authenticated:
            return redirect(url_for('main.Home'))
      form = RequestResetForm()
      if form.validate_on_submit():
            user = User.query.filter_by(email= form.email.data).first()
            send_reset_email(user)
            flash('an email has been sent to your inbox containing a reset token', 'info')
            return redirect(url_for('users.login'))
      return render_template('reset_request.html' ,title='reset password ' ,form = form ) 

@users.route('/reset_password/<token>' ,methods=['GET','POST'])
def reset_token(token):
      if current_user.is_authenticated:
            return redirect(url_for('main.Home'))
      user = User.verify_reset_token(token)
      if user is None:
            flash('invalid token', 'warning')
            return redirect(url_for('users.reset_request'))
      form = ResetPasswordForm()
      if form.validate_on_submit():
           hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf_8')
           user = User(username = form.username.data, email = form.email.data, password = hashed_password )
           user.password = hashed_password
           db.session.commit()
           flash(f'account updated for{form.username.data}!','success' )
           return redirect(url_for('users.login'))
   
      return render_template('reset_token.html', title='Reset password' ,form = form ) 
@users.route('/tenant')
@login_required
def rent():
    # Get the current user
    user = current_user

    # Get the most recent rent payment for the user
    latest_rent_payment = RentPayment.query.filter_by(tenant_id=user.id).order_by(RentPayment.date.desc()).first()

    # Calculate the total rent paid and rent balance
    total_paid = user.get_total_rent_paid()
    rent_amount = latest_rent_payment.amount if latest_rent_payment else 000  # default rent amount
    balance = user.get_rent_balance(rent_amount=rent_amount)

    # Render the rent template with the data
    return render_template('user_rent.html', total_paid=total_paid, balance=balance, user=user)

