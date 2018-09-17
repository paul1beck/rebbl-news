from flask import render_template, Blueprint
from flaskblog.models import Post


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET'])
def home():
    posts = Post.query.filter_by(published=True).order_by(Post.date_posted.desc())
    return render_template('home.html', posts=posts)

@main.route("/unpublished")
def unpublished():
    posts = Post.query.filter_by(published=False).order_by(Post.date_posted.desc())
    return render_template('home.html', posts=posts)

@main.route("/<string:category>")
def category(category):
    posts = Post.query.filter(Post.category==category,Post.published==True).order_by(Post.date_posted.desc())
    return render_template('home.html', posts=posts)
