from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('League', choices=[('All', 'All'), ('Big O', 'Big O'), ('GMAN', 'GMAN'), ('REL', 'REL'), ('Clan', 'Clan')])
    shortdesc = TextAreaField('Short Description', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    content = StringField('Add a Comment', validators=[DataRequired()])
    submit = SubmitField('Post')


class VideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('League', choices=[('All', 'All'), ('Big O', 'Big O'), ('GMAN', 'GMAN'), ('REL', 'REL'), ('Clan', 'Clan')])
    shortdesc = TextAreaField('Short Description', validators=[DataRequired()])
    video = TextAreaField('Short Description', validators=[DataRequired()])
    videotype = SelectField('League', choices=[('youtube', 'YouTube Video'), ('twitchvod', 'Twitch Vod'), ('twitchclip', 'Twitch Clip')])
    submit = SubmitField('Post')
