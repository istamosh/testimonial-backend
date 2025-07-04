from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, URL, Optional

class TestimonialForm(FlaskForm):
    class Meta:
        # Disable CSRF as this is an API endpoint
        csrf = False

    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(max=60, message='First name must not exceed 60 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(max=60, message='Last name must not exceed 60 characters')
    ])
    role_company = StringField('Role/Company', validators=[
        Length(max=120, message='Role/Company must not exceed 120 characters')
    ])
    profile_link = StringField('Professional Profile Link', validators=[
        DataRequired(message='Profile link is required'),
        Length(min=1, message='Profile link cannot be empty'),
        URL(message='Please enter a valid URL (e.g., https://linkedin.com/in/yourname)'),
        Length(max=500, message='Profile link must not exceed 500 characters')
    ])
    testimonial = TextAreaField('Testimonial', validators=[
        DataRequired(message='Testimonial message is required'),
        Length(min=10, message='Testimonial must be at least 10 characters long')
    ])
    censor_first_name = BooleanField('Censor first name', default=False)
    censor_last_name = BooleanField('Censor last name', default=False)
    consent_given = BooleanField('Consent given', validators=[
        DataRequired(message='Consent is required')
    ])

__all__ = ['TestimonialForm']
