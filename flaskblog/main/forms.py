from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

class RecapSelect(FlaskForm):
    category = SelectField(
        "League",
        choices=[
            ("Big O", "Big O"),
            ("GMAN", "GMAN"),
            ("REL", "REL"),
            ("Rookie", "Rookie")
        ],
    )
    division = SelectField(
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
    submit = SubmitField("Search")
