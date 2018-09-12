from flask import render_template, request, Blueprint
from flaskblog.models import Post, User


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", methods=['GET'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(published=True).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', posts=posts)

@main.route("/redesign", methods=['GET'])
def redesign():
    posts = Post.query.filter_by(published=True).order_by(Post.date_posted.desc())
    return render_template('home2.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/unpublished")
def unpublished():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(published=False).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', posts=posts)

@main.route("/clan")
def clan():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.category.in_(["Clan","All"])).filter_by(published=True).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', posts=posts)

@main.route("/clan/only", methods=['GET'])
def clan_only():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="Clan", published=True).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', posts=posts)

@main.route("/rel")
def rel():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.category.in_(["REL","All"])).filter_by(published=True).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('rel.html', posts=posts)

@main.route("/rel/only", methods=['GET'])
def rel_only():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="REL", published=True).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('rel.html', posts=posts)

@main.route("/gman")
def gman():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.category.in_(["GMAN","All"])).filter_by(published=True).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('gman.html', posts=posts)

@main.route("/gman/only", methods=['GET'])
def gman_only():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="GMAN", published=True).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('gman.html', posts=posts)

@main.route("/big-o")
def bigo():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.category.in_(["Big O","All"])).filter_by(published=True).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('bigo.html', posts=posts)

@main.route("/big-o/only", methods=['GET'])
def bigo_only():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category="Big O", published=True).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('bigo.html', posts=posts)