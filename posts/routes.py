from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from datetime import datetime

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, category=form.category.data, 
                    shortdesc=form.shortdesc.data, content=form.content.data, 
                    author=current_user, published=False)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, shortdesc=post.shortdesc, post=post)

@posts.route("/post2/<int:post_id>")
def post2(post_id):
    post = Post.query.get_or_404(post_id)
    category = post.category
    posts = Post.query.filter(Post.id!=post_id, Post.category==category,Post.published==True).order_by(Post.date_posted.desc()).limit(5)
    return render_template('post2.html', title=post.title, shortdesc=post.shortdesc, post=post, posts=posts)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = form.category.data
        post.shortdesc = form.shortdesc.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.category.data = post.category
        form.shortdesc.data = post.shortdesc
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route("/post/<int:post_id>/publish", methods=['POST'])
@login_required
def publish_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        redirect(url_for('posts.post', post_id=post.id))
    post.published = True
    post.date_posted = datetime.utcnow()
    db.session.commit()
    flash('Your post has been Published!', 'success')
    return redirect(url_for('posts.post', post_id=post.id))

@posts.route("/post/<int:post_id>/unpublish", methods=['POST'])
@login_required
def unpublish_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        redirect(url_for('posts.post', post_id=post.id))
    post.published = False
    db.session.commit()
    flash('Your post has been Unpublished!', 'success')
    return redirect(url_for('posts.post', post_id=post.id))