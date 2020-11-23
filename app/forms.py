from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField
from wtforms.fields.html5 import EmailField  
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    #validation method possibly use for another
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class BoardForm(FlaskForm):
    title = StringField('New Board Title', validators=[DataRequired()])
    submit = SubmitField('Create')

class CardForm(FlaskForm):
    header = StringField('Card Header', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Create')

class TaskForm(FlaskForm):
    card_id = IntegerField('Cardid', validators=[DataRequired()])
    tasktext = StringField('Task', validators=[DataRequired()])
    submit = SubmitField('+')

class DeleteTaskForm(FlaskForm):
    id = IntegerField('Taskid', validators=[DataRequired()])
    submit = SubmitField('-')

# class DeleteCardForm(FlaskForm):
#     id = IntegerField('Taskid', validators=[DataRequired()])
#     submit = SubmitField('-')