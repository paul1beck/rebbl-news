class Config:
    SECRET_KEY = '14e6c09c271660f566450fcb09705a3f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'rebblnews@gmail.com'
    MAIL_PASSWORD = 'fakenews'
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_HEIGHT = 400