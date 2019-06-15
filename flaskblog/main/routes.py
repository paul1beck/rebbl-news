from flask import render_template, url_for, redirect, request, Blueprint
from flaskblog.models import Post
from flaskblog.main.forms import RecapSelect

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=["GET", "POST"])
def home():
    form = RecapSelect()
    if form.validate_on_submit():
        return redirect(url_for('main.recap', category=form.category.data, division=form.division.data))
    posts = Post.query.filter(Post.published==True, Post.post_type!='recap').order_by(Post.date_posted.desc())
    return render_template('home.html', posts=posts, form=form)

@main.route("/unpublished")
def unpublished():
    posts = Post.query.filter_by(published=False).order_by(Post.date_posted.desc())
    return render_template('home.html', posts=posts)

@main.route("/<string:category>")
def category(category):
    posts = Post.query.filter(Post.category==category,Post.published==True, Post.post_type!='recap').order_by(Post.date_posted.desc())
    return render_template('home.html', posts=posts)

@main.route("/recap/", methods=["GET", "POST"])
def all_recap():
    form = RecapSelect()
    if form.validate_on_submit():
        return redirect(url_for('main.recap', category=form.category.data, division=form.division.data))
    posts = Post.query.filter(Post.published==True, Post.post_type=='recap').order_by(Post.week.desc())
    return render_template('recap_home.html', posts=posts, form=form)

@main.route("/recap/<string:category>/<string:division>", methods=["GET", "POST"])
def recap(category, division):
    form = RecapSelect()
    if form.validate_on_submit():
        return redirect(url_for('main.recap', category=form.category.data, division=form.division.data))
    elif request.method == "GET":
        form.category.data = category
        form.division.data = division
    posts = Post.query.filter(Post.published==True, Post.post_type=='recap', Post.category==category).filter(Post.division.contains(division)).order_by(Post.week.desc())
    return render_template('recap_home.html', posts=posts, form=form)