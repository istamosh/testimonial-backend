from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class PreservedTestimonialForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=2, max=120, message="Name must be between 2 and 120 characters")
    ])
