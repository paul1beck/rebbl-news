from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from flask_admin import Admin
from flaskblog.admin import AdminView
from flask_ckeditor import CKEditor

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()
admin = Admin()
ckeditor = CKEditor()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        from flaskblog.models import User, UserRole, Post, PostComment

        db.create_all()
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    admin = Admin(
        app,
        name="Dashboard",
        index_view=AdminView(User, db.session, url="/admin", endpoint="admin"),
    )
    admin.add_view(AdminView(UserRole, db.session))
    admin.add_view(AdminView(Post, db.session))
    admin.add_view(AdminView(PostComment, db.session))
    return app
