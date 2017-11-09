# -*- coding:utf-8 -*-

from flask import render_template, redirect, request, url_for, flash, \
    current_app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from . import auth
from .forms import LoginForm, RegistrationForm, RestPWDForm
from .. import db, oid, login_manager
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter(or_(
            User.email == form.login.data,
            User.phone == form.login.data)).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)

            next_request = request.args.get('next')
            return redirect(next_request or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/rest-pwd', methods=['GET', 'POST'])
@login_required
def reset_pwd():
    form = RestPWDForm()

    if form.validate_on_submit():
        if current_user.verify_password(form.password_current.data):
            current_user.password = form.password_new.data
            flash("Success. Your password have change. Please login again.")
            logout_user()
            return redirect(url_for('auth.login'))
        else:
            flash("Fail. Your current password was wrong.")

    return render_template('auth/reset_password.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
