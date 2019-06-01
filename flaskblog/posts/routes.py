from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, PostComment, Video, VideoComment
from flaskblog.posts.forms import PostForm, CommentForm, VideoForm
from flaskblog.posts.utils import save_picture
from datetime import datetime
from slugify import slugify


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Working on adding Cover Photos
        '''if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.image_file = picture_file'''
        post = Post(title=form.title.data, category=form.category.data,
                    shortdesc=form.shortdesc.data, content=form.content.data,
                    author=current_user, published=False, sidebar=True)
        # cover_image=post.image_file)
        db.session.add(post)
        db.session.commit()
        post.slug = (slugify(form.title.data, max_length=35).lower() + "-" + str(post.id))
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('posts.postslug', post_slug=post.slug))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post_id = post.id
    category = post.category
    comments = PostComment.query.filter(PostComment.post_id == post_id).order_by(PostComment.date_posted.asc())
    posts = Post.query.filter(Post.id != post_id, Post.category == category, Post.published == True).order_by(Post.date_posted.desc()).limit(6)
    form = CommentForm()
    if form.validate_on_submit():
        comment = PostComment(content=form.content.data, user=current_user, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('posts.postslug', _anchor='commentsection', post_slug=post.slug))

    return render_template('post.html', form=form, title=post.title, shortdesc=post.shortdesc, post=post, posts=posts, comments=comments)


@posts.route("/post/<string:post_slug>", methods=['GET', 'POST'])
def postslug(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    post_id = post.id
    comments = PostComment.query.filter(PostComment.post_id == post_id).order_by(PostComment.date_posted.asc())
    category = post.category
    posts = Post.query.filter(Post.id != post_id, Post.category == category, Post.published == True).order_by(Post.date_posted.desc()).limit(5)
    form = CommentForm()
    if form.validate_on_submit():
        comment = PostComment(content=form.content.data, user=current_user, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('posts.postslug', _anchor='commentsection', post_slug=post.slug))

    return render_template('post.html', form=form, title=post.title, shortdesc=post.shortdesc, post=post, posts=posts, comments=comments)


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
        return redirect(url_for('posts.postslug', post_slug=post.slug))
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
    return redirect(url_for('posts.postslug', post_slug=post.slug))


@posts.route("/post/<int:post_id>/unpublish", methods=['POST'])
@login_required
def unpublish_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        if current_user.role != "Admin":
            redirect(url_for('posts.postslug', post_slug=post.slug))
    post.published = False
    db.session.commit()
    flash('Your post has been Unpublished!', 'success')
    return redirect(url_for('posts.postslug', post_slug=post.slug))


@posts.route("/postcomment/<int:post_id>/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id, post_id):
    comment = PostComment.query.get_or_404(comment_id)
    post = Post.query.get_or_404(post_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment has been deleted!', 'success')
    return redirect(url_for('posts.postslug', post_slug=post.slug))

### VIDEO SECTION ###

@posts.route("/video/new", methods=['GET', 'POST'])
@login_required
def new_video():
    form = VideoForm()
    if form.validate_on_submit():
        #Insert logic to parse out video unique identifier to store as video
        videourl = form.video.data
        video = Video(title=form.title.data, category=form.category.data,
                    shortdesc=form.shortdesc.data, video=videourl, videotype=form.videotype.data,
                    recap=form.recap.data, division=form.division.data, week=form.week.data,
                    author=current_user, published=False, sidebar=True)
        db.session.add(video)
        db.session.commit()
        video.slug = (slugify(form.title.data, max_length=35).lower() + "-" + str(video.id))
        db.session.commit()
        flash('Your video has been added!', 'success')
        return redirect(url_for('posts.video', video_slug=video.slug))
    return render_template('create_video_post.html', title='New Video Post',
                           form=form, legend='New Video Post')


@posts.route("/video/<int:video_id>/update", methods=['GET', 'POST'])
@login_required
def update_video(video_id):
    video = Video.query.get_or_404(video_id)
    if video.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        video.title = form.title.data
        video.category = form.category.data
        video.shortdesc = form.shortdesc.data
        video.video = form.video.data
        video.videotype = form.videotype.data
        video.recap = form.recap.data
        video.division = form.division.data
        video.week = form.week.data
        db.session.commit()
        flash('Your video post has been updated!', 'success')
        return redirect(url_for('posts.video', video_slug=video.slug))
    elif request.method == 'GET':
        form.title.data = video.title
        form.category.data = video.category
        form.shortdesc.data = video.shortdesc
        form.video.data = video.video
        form.videotype.data = video.videotype
        form.recap.data = video.recap
        form.division.data = video.division
        form.week.data = video.week
    return render_template('create_video.html', title='Update Video Post',
                           form=form, legend='Update Video Post')

@posts.route("/video/<string:video_slug>", methods=['GET', 'POST'])
def video(video_slug):
    video = Video.query.filter_by(slug=video_slug).first()
    video_id = video.id
    comments = VideoComment.query.filter(VideoComment.video_id == video_id).order_by(VideoComment.date_posted.asc())
    category = video.category
    videos = Video.query.filter(Video.id != video_id, Video.category == category, Video.division == video.division,
        Video.published == True).order_by(Video.date_posted.desc()).limit(5)
    form = CommentForm()
    if form.validate_on_submit():
        comment = VideoComment(content=form.content.data, user=current_user, video_id=video.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('posts.video', _anchor='commentsection', video_slug=video.slug))

    return render_template('video.html', form=form, title=video.title, shortdesc=video.shortdesc, video=video, videos=videos, comments=comments)

@posts.route("/video/<int:video_id>/delete", methods=['POST'])
@login_required
def delete_video(video_id):
    video = Video.query.get_or_404(post_id)
    if video.author != current_user:
        abort(403)
    db.session.delete(video)
    db.session.commit()
    flash('Your video post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/video/<int:video_id>/publish", methods=['POST'])
@login_required
def publish_video(video_id):
    video = Video.query.get_or_404(video_id)
    if video.author != current_user:
        redirect(url_for('posts.video', video_slug=video.slug))
    video.published = True
    video.date_posted = datetime.utcnow()
    db.session.commit()
    flash('Your video post has been Published!', 'success')
    return redirect(url_for('posts.video', video_slug=video.slug))


@posts.route("/video/<int:video_id>/unpublish", methods=['POST'])
@login_required
def unpublish_video(video_id):
    video = Video.query.get_or_404(video_id)
    if video.author != current_user:
        if current_user.role != "Admin":
            redirect(url_for('posts.video', video_slug=video.slug))
    video.published = False
    db.session.commit()
    flash('Your video post has been Unpublished!', 'success')
    return redirect(url_for('posts.video', video_slug=video.slug))


@posts.route("/videocomment/<int:video_id>/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_video_comment(comment_id, video_id):
    comment = VideoComment.query.get_or_404(comment_id)
    video = Video.query.get_or_404(video_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment has been deleted!', 'success')
    return redirect(url_for('posts.video', video_slug=video.slug))
