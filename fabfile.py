from fabric.api import run, local

def host_type():
    run('uname -s')


def hello():
    print "hello world!"

def ls(path='.'):
    local('ls {}',format(path))

def prepare_deploy():
    #local("python manage.py test my_app")
    local("git add -i && git commit -p --interactive")
    local("git push")
