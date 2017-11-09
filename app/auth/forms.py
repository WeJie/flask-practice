# -*- coding:utf-8 -*-

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, Email, Regexp, EqualTo, URL, DataRequired
from wtforms import ValidationError

from ..models import User


class OpenIDForm(FlaskForm):
    openid = StringField('OpenID URL', [DataRequired(), URL()])


class LoginForm(FlaskForm):
    login = StringField('Email/Phone', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RestPWDForm(FlaskForm):
    password_current = PasswordField('Current Password', validators=[DataRequired()])
    password_new = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8),
        EqualTo('password_confirm', message='Passwords must match.')
    ])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Reset')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                   'Usernames must have only letters, number, dots or undersores')])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        EqualTo('password2', message='Passwords must match.')
    ])
    password2 = PasswordField('confirm password', validators=[DataRequired()])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in user.')

    # def validate(self):
    #     check_validate = super(RegistrationForm, self).validate()
        
    #     if not check_validate:
    #         return False

    #     user = User.query.filter_by(
    #         username=self.username.data
    #     ).first()
    #     if user:
    #         self.username.errors.append('User with that name already exists')
    #         return False

    #     return True


