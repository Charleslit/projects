from flask import Blueprint 
from  flask import (render_template, url_for, flash, redirect, request, abort, )
from flask_login import current_user, login_required
from rms import db
from rms.models import Post
from rms.posts.forms import PostForm


posts = Blueprint('posts', __name__)

@posts.route('/post/new' ,methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
      post = Post(title= form.title.data, content = form.content.data, author = current_user)
      db.session.add(post)
      db.session.commit()

      flash('your post has been created', 'success')
      return redirect(url_for('main.Home'))
    return render_template('posts.html', title='newpost' , form = form , legend = new_post ) 
    
@posts.route('/post/<int:post_id>')
def post(post_id):
        posts = Post.query.get_or_404(post_id)
        return render_template('post.html',title=posts.title,posts=posts )

@posts.route('/post/<int:post_id>/update', methods=['GET','POST'] )
@login_required
def update_post(post_id):
            posts = Post.query.get_or_404(post_id)
            if posts.author != current_user:
             abort(403)
            form = PostForm()
            if form.validate_on_submit():
                  posts.title = form.title.data
                  posts.content = form.content.data
                  db.session.commit()
                  flash('your post has been updated', 'success')
                  return redirect(url_for('posts.post',post_id = posts.id))
            elif request.method == 'GET':
             
             form.title.data =posts.title
             form.content.data = posts.content

            return render_template('posts.html',title='update post',form = form, legend = update_post )

@posts.route('/post/<int:post_id>/delete', methods=['POST'] )
@login_required
def delete_post(post_id):
      post = Post.query.get_or_404(post_id)
      if post.author != current_user:
            abort(403)
      db.session.delete(post)
      db.session.commit()
      flash('your post has been deleted !', 'success') 
      return redirect(url_for('main.Home'))     
 