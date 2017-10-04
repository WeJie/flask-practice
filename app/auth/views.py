# -*- coding:utf-8 -*-

from flask import render_template, redirect, request, url_for, flash, \
    current_app, session
from flask_login import login_user,logout_user, login_required, current_user
from sqlalchemy import or_

from . import auth
from .forms import LoginForm, RegistrationForm, OpenIDForm
from .. import db, oid, login_manager
from ..models import User
from ..email import send_email
from ..extensions import twitter 


@auth.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    # openid_form = OpenIDForm()
    
    # if openid_form.validate_on_submit():
    #     return oid.try_login(
    #         openid_form.openid.data,
    #         ask_for=['nickname', 'email'],
    #         ask_for_optional=['fullname']
    #     )

    if form.validate_on_submit():

        user = User.query.filter(or_(
            User.email == form.login.data,
            User.phone == form.login.data)).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)

            # identity_changed(
            #     current_app._get_current_object(),
            #     identity=Identity(user.id)
            # )

            next_request = request.args.get('next')
            return redirect(next_request or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/twitter-login')
def twitter_login():
    print 'twitter here', twitter
    twitter_auth = twitter.authorize(
        callback=url_for('.twitter_authorized',
        next=request.referrer or None,
        _external=True
        )
    )
    print 'twitter auth here', twitter_auth
    return twitter_auth
    
    # return twitter.authorize(callback=url_for('.twitter_authorized',
    #     next=request.args.get('next') or request.referrer or None))


@auth.route('/twitter-login/authorized')
@twitter.authorized_handler
def twitter_authorized(resp):
    print 'twitter callback here'
    if resp is None:
        return 'Access denied: reason: {} error: {}'.format(
            requset.args['error_reason'],
            request.args['error_description']
        )
    session['twitter_oauth_token'] = resp['oauth_token'] + resp['oauth_token_secret']

    user = User.query.filter_by(
        username=resp['screen_name']
    )

    if not user:
        user = User(resp['screen_name'], '')
        db.session.add(user)
        db.session.commit()

    flask("You have been logged in.", category="success")
    return redirect(
        request.args.get('next') or url_for('blog.home')
    )

@auth.route('/logout')
@login_required
def logout():
    logout_user()

    # identity_changed(
    #     current_app._get_current_object(),
    #     identity=AnonymousIdentity()
    # )

    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmaton_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'auth/email/confirm', user=user, token=token)
        # flash('A confirmation email has been sent to your email.')
        # return redirect(url_for('main.index'))
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template(
        'auth/register.html', 
        form=form, 
        public_key=current_app.config['RECAPTCHA_PUBLIC_KEY'])

@auth.route('/conifrm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confrim(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmaton_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to your email address.')

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        # if not current_user.confirmed \
        #     and request.endpoint[:5] != 'auth.' \
        #     and request.endpoint != 'static':

        #     return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')
