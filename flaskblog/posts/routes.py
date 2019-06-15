from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, PostComment
from flaskblog.posts.forms import PostForm, CommentForm, VideoForm, RecapForm
from flaskblog.posts.utils import save_picture, parse_video_url, parse_video_img
from datetime import datetime
from slugify import slugify


posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Working on adding Cover Photos
        """if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.image_file = picture_file"""
        post = Post(
            title=form.title.data,
            category=form.category.data,
            shortdesc=form.shortdesc.data,
            content=form.content.data,
            author=current_user,
            published=False,
            sidebar=True,
            post_type="text",
        )
        # cover_image=post.image_file)
        db.session.add(post)
        db.session.commit()
        post.slug = slugify(form.title.data, max_length=35).lower() + "-" + str(post.id)
        db.session.commit()
        flash("Your comment has been added!", "success")
        return redirect(url_for('posts.postslug', post_slug=post.slug))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@posts.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post_id = post.id
    category = post.category
    comments = PostComment.query.filter(PostComment.post_id == post_id).order_by(
        PostComment.date_posted.asc()
    )
    posts = (
        Post.query.filter(
            Post.id != post_id, Post.category == category, Post.published == True
        )
        .order_by(Post.date_posted.desc())
        .limit(6)
    )
    form = CommentForm()
    if form.validate_on_submit():
        comment = PostComment(
            content=form.content.data, user=current_user, post_id=post.id
        )
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added!", "success")
        return redirect(
            url_for("posts.postslug", _anchor="commentsection", post_slug=post.slug)
        )

    return render_template(
        "post.html",
        form=form,
        title=post.title,
        shortdesc=post.shortdesc,
        post=post,
        posts=posts,
        comments=comments,
    )


@posts.route("/post/<string:post_slug>", methods=["GET", "POST"])
def postslug(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()
    post_id = post.id
    comments = PostComment.query.filter(PostComment.post_id == post_id).order_by(
        PostComment.date_posted.asc()
    )
    category = post.category
    posts = (
        Post.query.filter(
            Post.id != post_id, Post.category == category, Post.published == True
        )
        .order_by(Post.date_posted.desc())
        .limit(5)
    )
    form = CommentForm()
    if form.validate_on_submit():
        comment = PostComment(
            content=form.content.data, user=current_user, post_id=post.id
        )
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added!", "success")
        return redirect(
            url_for('posts.postslug', _anchor="commentsection", post_slug=post.slug)
        )

    if post.post_type == "text":
        return render_template(
            "post.html",
            form=form,
            title=post.title,
            shortdesc=post.shortdesc,
            post=post,
            posts=posts,
            comments=comments,
        )
    elif post.post_type == "video":
        return render_template(
            "video.html",
            form=form,
            title=post.title,
            shortdesc=post.shortdesc,
            post=post,
            posts=posts,
            comments=comments,
        )
    elif post.post_type == "recap":
        return render_template(
            "recap.html",
            form=form,
            title=post.title,
            post=post,
            posts=posts,
            comments=comments,
        )

@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
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
        flash("Your post has been updated!", "success")
        return redirect(url_for("posts.postslug", post_slug=post.slug))
    elif request.method == "GET":
        form.title.data = post.title
        form.category.data = post.category
        form.shortdesc.data = post.shortdesc
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))


@posts.route("/post/<int:post_id>/publish", methods=["POST"])
@login_required
def publish_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        redirect(url_for("posts.post", post_id=post.id))
    post.published = True
    post.date_posted = datetime.utcnow()
    db.session.commit()
    flash("Your post has been Published!", "success")
    return redirect(url_for("posts.postslug", post_slug=post.slug))


@posts.route("/post/<int:post_id>/unpublish", methods=["POST"])
@login_required
def unpublish_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        if current_user.role != "Admin":
            redirect(url_for("posts.postslug", post_slug=post.slug))
    post.published = False
    db.session.commit()
    flash("Your post has been Unpublished!", "success")
    return redirect(url_for("posts.postslug", post_slug=post.slug))


@posts.route("/postcomment/<int:post_id>/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id, post_id):
    comment = PostComment.query.get_or_404(comment_id)
    post = Post.query.get_or_404(post_id)
    db.session.delete(comment)
    db.session.commit()
    flash("Comment has been deleted!", "success")
    return redirect(url_for("posts.postslug", post_slug=post.slug))


### VIDEO SECTION ###


@posts.route("/video/new", methods=["GET", "POST"])
@login_required
def new_video():
    form = VideoForm()
    if form.validate_on_submit():
        # Insert logic to parse out video unique identifier to store as video
        videoinput = form.video.data
        post = Post(
            title=form.title.data,
            category=form.category.data,
            shortdesc=form.shortdesc.data,
            content=form.content.data,
            video=form.video.data,
            # post.videotype = form.videotype.data,
            videoimg=parse_video_img(videoinput),
            videourl=parse_video_url(videoinput),
            author=current_user,
            post_type="video",
            published=False,
            sidebar=True,
        )
        db.session.add(post)
        db.session.commit()
        post.slug = slugify(form.title.data, max_length=35).lower() + "-" + str(post.id)
        db.session.commit()
        flash("Your video has been added!", "success")
        return redirect(url_for("posts.postslug", post_slug=post.slug))
    return render_template(
        "create_video.html",
        title="New Video Post",
        form=form,
        legend="New Video Post",
    )


@posts.route("/video/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_video(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = VideoForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.shortdesc = form.shortdesc.data
        post.video = form.video.data
        videoinput = form.video.data
        post.videoimg = parse_video_img(videoinput)
        post.videourl = parse_video_url(videoinput)
        db.session.commit()
        flash("Your video post has been updated!", "success")
        return redirect(url_for("posts.postslug", post_slug=post.slug))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category
        form.shortdesc.data = post.shortdesc
        form.video.data = post.video
    return render_template(
        "create_video.html",
        title="Update Video Post",
        form=form,
        legend="Update Video Post",
    )

@posts.route("/recap/new", methods=["GET", "POST"])
@login_required
def new_recap():
    form = RecapForm()
    if form.validate_on_submit():
        videoinput = form.video.data
        title_str = f'{form.category.data} - Division {form.division.data} - Week {form.week.data}'
        post = Post(
            title = title_str,
            category=form.category.data,
            content = form.content.data,
            shortdesc = form.shortdesc.data,
            video=form.video.data,
            videoimg=parse_video_img(videoinput),
            videourl=parse_video_url(videoinput),
            division=", ".join(form.division.data),
            week=form.week.data,
            author=current_user,
            post_type="recap",
            published=False,
            sidebar=True,
        )
        db.session.add(post)
        db.session.commit()
        post.slug = slugify(str(title_str), max_length=35).lower() + "-" + str(post.id)
        db.session.commit()
        flash("Your Recap Video has been added!", "success")
        return redirect(url_for("posts.postslug", post_slug=post.slug))
    return render_template(
        "create_recap.html",
        title="New Video Recap",
        form=form,
        legend="New Video Recap",
    )


@posts.route("/recap/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_recap(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = RecapForm()
    if form.validate_on_submit():
        post.title = f'{form.category.data} - Division {form.division.data} - Week {form.week.data}'
        post.content = form.content.data
        post.category = form.category.data
        post.shortdesc = form.shortdesc.data
        post.video = form.video.data
        videoinput = form.video.data
        post.videoimg = parse_video_img(videoinput)
        post.videourl = parse_video_url(videoinput)
        post.division = ", ".join(form.division.data)
        post.week = form.week.data
        db.session.commit()
        flash("Your Recap Video has been updated!", "success")
        return redirect(url_for("posts.postslug", post_slug=post.slug))
    elif request.method == "GET":
        form.content.data = post.content
        form.shortdesc.data = post.shortdesc
        form.category.data = post.category
        form.video.data = post.video
        form.division.data = post.division.split(", ")
        form.week.data = post.week
    return render_template(
        "create_recap.html",
        title="Update Video Recap",
        form=form,
        legend="Update Video Recap",
    )