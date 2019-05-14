from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, optional
import os


class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')

class RegForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Your Password Again', validators=[DataRequired()])
    submit = SubmitField('Sign up')

class AddTaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], coerce=int)
    date = DateTimeField('Deadline', validators=[DataRequired()])
    user = SelectField('Delegate to:', coerce=int)
    submit = SubmitField('Add')