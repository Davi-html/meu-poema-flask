import flask_wtf
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class SignupForm(flask_wtf.FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')


class SigninForm(flask_wtf.FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    rememberPassword = BooleanField('Lembrar dados de acesso')
    submit = SubmitField('Submit')