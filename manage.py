#! /usr/bin/env python

import os 
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage 
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db
from app.models import User, Role, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLAK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest 
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covidr = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(direcotry=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app, 
        restrictions=[length], 
        profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    upgrade()


@manager.command
def setup_db():

    admin_role = Role()
    admin_role.name = 'admin'
    db.session.add(admin_role)

    default_role = Role()
    default_role.name = 'default'
    db.session.add(default_role)

    admin = User()
    admin.username = 'admin'
    admin.password = 'password'
    admin.roles.append(admin_role)
    db.session.add(admin)

    db.session.commit()

if __name__ == '__main__':
    manager.run()

