from flask import Blueprint , render_template, request  
from rms.models import Post

users = Blueprint('users', __name__)
@main.route("/Home")
def Home():
      page = request.args.get('page',1, type= int)
      posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page ,per_page=5)
      return render_template('Home.html', posts=posts)

@main.route('/About')
def about():
      return render_template('About.html', title='About')

@main.route('/users')
@login_required
def users():
       users =  User.query.all()
       return render_template('users.html', title='users', users=users) 

