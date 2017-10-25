# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, abort, flash,\
    request, current_app, make_response
from flask_login import current_user, login_required
from flask_sqlalchemy import get_debug_queries
from flask_principal import Permission, RoleNeed

from . import main
from .. import db
from .forms import PostForm, NameForm, EditProfileForm, EditProfileAdminForm, CommentForm
from ..models import User, Post, Comment#, Permission
from ..decorators import admin_required, permission_required

test_permission = Permission(RoleNeed('tester'))


@main.route('/re_test', methods=['GET', 'POST'])
@test_permission.require()
def re_test():
    return render_template('only you are tester')


@main.route('/re_test2', methods=['GET', 'POST'])
def re_test2():
    print 'Hello World'
    with test_permission.require():
        return render_template('only you are tester2')


@main.route('/', methods=['GET', 'POST'])
def index():
    query = Post.query
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POST_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)


@main.route('/archive/')
def archive():
    return render_template('archive.html', posts=[])


@main.route('/tags/')
def tags():
    return "I'm tags."


@main.route('/about/')
def about():
    return "I'm about."


@main.route('/hello')
def hello():
    return "Hello"


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/post/new/', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            body=form.body.data,
            author=current_user._get_current_object()
        )
        db.session.add(post)
        return redirect(url_for('.index'))
    return render_template('new_post.html', form=form)


@main.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(404)

    form = PostForm()

    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', post_id=post.id))

    form.body.data = post.body
    form.title.data = post.title
    return render_template('edit_post.html', form=form)


@main.route('/post/<int:post_id>', methods=['GET','POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data,
            post=post,
            author=current_user._get_current_object()
        )
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', post_id=post.id, page=-1))

    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template('post.html', post=post, form=form,
                           comments=comments, pagination=pagination)


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s \n Parameters: %s\n Duration: %fs\nContext: %s\n' %
                (query.statement, query.parameters, query.duration, query.context)
            )
    return response





