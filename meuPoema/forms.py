import flask_wtf
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from meuPoema.models import User


class SignupForm(flask_wtf.FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já cadastrado')


class SigninForm(flask_wtf.FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    rememberPassword = BooleanField('Lembrar dados de acesso')
    submit = SubmitField('Submit')

class FormEditProfile(flask_wtf.FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    email = EmailField('Email',validators=[DataRequired(), Email()])
    foto_perfil = FileField('Foto de Perfil',validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens são permitidas!')])
    submit = SubmitField('Editar')

class FollowForm(flask_wtf.FlaskForm):
    follow = SubmitField('Seguir')
    unfollow = SubmitField('Deixar de seguir')

class SaveConfig(flask_wtf.FlaskForm):
    submit = SubmitField('Salvar')
    checkboxNotifications = BooleanField('Ativar notificações')
    checkboxRanking = BooleanField('Ativar ranking')