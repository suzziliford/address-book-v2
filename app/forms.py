from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField
from wtforms.validators import EqualTo, InputRequired  


class SignUpForm(FlaskForm):
    # first_name = StringField('First Name', validators=[InputRequired()])
    # last_name = StringField('Last Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField()

class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    phone_number = StringField('Phone Number', validators=[InputRequired()])
    submit = SubmitField()