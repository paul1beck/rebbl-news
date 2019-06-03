from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = SelectField(
        "League",
        choices=[
            ("All", "All"),
            ("Big O", "Big O"),
            ("GMAN", "GMAN"),
            ("REL", "REL"),
            ("Clan", "Clan"),
        ],
    )
    shortdesc = TextAreaField("Short Description", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class VideoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = SelectField(
        "League",
        choices=[
            ("All", "All"),
            ("Big O", "Big O"),
            ("GMAN", "GMAN"),
            ("REL", "REL"),
            ("Clan", "Clan"),
        ],
    )
    shortdesc = TextAreaField("Short Description", validators=[DataRequired()])
    content = CKEditorField("Content")
    video = TextAreaField("Video URL", validators=[DataRequired()])
    videotype = SelectField(
        "Video Type",
        choices=[
            ("youtube", "YouTube Video"),
            ("twitchvod", "Twitch Vod"),
            ("twitchclip", "Twitch Clip"),
        ],
        validators=[DataRequired()],
    )
    recap = BooleanField("Weekly Recap")
    division = SelectField(
        "Division",
        choices=[
            ("none", "None"),
            ("1", "1"),
            ("2a", "2A"),
            ("2b", "2B"),
            ("3a", "3A"),
            ("3b", "3B"),
            ("3c", "3C"),
            ("4a", "4A"),
            ("4b", "4B"),
            ("4c", "4C"),
            ("4d", "4D"),
            ("4e", "4E"),
            ("4F", "4F"),
            ("5a", "5A"),
            ("5b", "5B"),
            ("5c", "5C"),
            ("5d", "5D"),
            ("5e", "5E"),
            ("5f", "5F"),
            ("5G", "5G"),
        ],
    )
    week = SelectField(
        "Week",
        choices=[
            (0, "Precap"),
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
            (6, "6"),
            (7, "7"),
            (8, "8"),
            (9, "9"),
            (10, "10"),
            (11, "11"),
            (12, "12"),
            (13, "13"),
            (14, "Post Season"),
        ],
    )
    submit = SubmitField("Post")


class CommentForm(FlaskForm):
    content = StringField("Add a Comment", validators=[DataRequired()])
    submit = SubmitField("Post")
