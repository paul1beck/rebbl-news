from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
    BooleanField,
    SelectMultipleField,
)
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
            ("Lineman", "Lineman"),
            ("Rookie", "Rookie"),
        ],
    )
    shortdesc = TextAreaField("Short Description", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Save")


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
            ("Lineman", "Lineman"),
            ("Rookie", "Rookie"),
        ],
    )
    shortdesc = TextAreaField("Short Description")
    content = CKEditorField("Content")
    video = TextAreaField("Video URL", validators=[DataRequired()])
    submit = SubmitField("Save")


class RecapForm(FlaskForm):
    category = SelectField(
        "League", choices=[("Big O", "Big O"), ("GMAN", "GMAN"), ("REL", "REL"), ("Rookie", "Rookie")]
    )
    shortdesc = TextAreaField(
        "OPTIONAL - Short Description (used in previews on Discord)"
    )
    content = CKEditorField("OPTIONAL - Content - Add any other information or links")
    video = TextAreaField("Video URL", validators=[DataRequired()])
    division = SelectMultipleField(
        "Division",
        choices=[
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
            ("4f", "4F"),
            ("5a", "5A"),
            ("5b", "5B"),
            ("5c", "5C"),
            ("5d", "5D"),
            ("5e", "5E"),
            ("5f", "5F"),
            ("5g", "5G"),
            ("5h", "5H"),
            ("5i", "5I"),
            ("5j", "5J"),
            ("5k", "5K"),
            ("Rookies", "Rookies"),
        ],
    )
    week = SelectField(
        "Week",
        choices=[
            ("00", "Precap"),
            ("01", "1"),
            ("02", "2"),
            ("03", "3"),
            ("04", "4"),
            ("05", "5"),
            ("06", "6"),
            ("07", "7"),
            ("08", "8"),
            ("09", "9"),
            ("10", "10"),
            ("11", "11"),
            ("12", "12"),
            ("13", "13"),
            ("14", "Post Season"),
        ],
    )
    submit = SubmitField("Save")


class CommentForm(FlaskForm):
    content = StringField("Add a Comment", validators=[DataRequired()])
    submit = SubmitField("Post")
