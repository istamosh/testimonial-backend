from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class SignupForm(FlaskForm):
    class Meta:
        # Disable CSRF as this is an API endpoint
        csrf = False
        
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    password = StringField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, max=100, message='Password must be between 6 and 100 characters')
    ])

class LoginForm(FlaskForm):
    class Meta:
        # Disable CSRF as this is an API endpoint
        csrf = False
        
    username = StringField('Username', validators=[
        DataRequired(message='Username is required')
    ])
    password = StringField('Password', validators=[
        DataRequired(message='Password is required')
    ])
