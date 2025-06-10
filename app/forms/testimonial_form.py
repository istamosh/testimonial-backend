from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, URL

class TestimonialForm(FlaskForm):
    class Meta:
        # Disable CSRF as this is an API endpoint
        csrf = False

    nameOrEmail = StringField('Name or Email', validators=[
        DataRequired(message='Name or Email is required'),
        Length(max=120, message='Name or Email must not exceed 120 characters')
    ])
    linkedinUrl = StringField('LinkedIn URL', validators=[
        DataRequired(message='LinkedIn URL is required'),
        URL(message='Invalid LinkedIn URL'),
        Length(max=255, message='LinkedIn URL must not exceed 255 characters')
    ])
    testimonial = TextAreaField('Testimonial', validators=[
        DataRequired(message='Testimonial message is required'),
        Length(min=10, message='Testimonial must be at least 10 characters long')
    ])

__all__ = ['TestimonialForm']
