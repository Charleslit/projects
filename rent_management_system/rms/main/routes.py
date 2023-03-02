from flask import Blueprint, render_template, request
from rms.models import Post, User, RentPayment

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/Home")
def Home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('Home.html', posts=posts)

@main.route('/About')
def about():
    return render_template('About.html', title='About')

@main.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', title='users', users=users)

@main.route('/rent')
def rent():
    rent = RentPayment.query.order_by(RentPayment.date.desc())
    return render_template('rent.html', title='rent', rent=rent)
