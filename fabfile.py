from fabric.api import *

def amy():
    env.user = 'axz'

def prod():
    env.hosts = ['wikum.csail.mit.edu']
    env.graceful = True
    env.server_path = '/opt/highlight'
    env.python_path = '/opt/virtualenvs/highlight/bin'
    return

def deploy():
   
    sudo("rm -rf %s/*" % env.server_path)
    local('zip -r code.zip * -x "*.pyc" "*.git"')
    put("code.zip", "%s/" % env.server_path, use_sudo=True)
    sudo("cd %s; unzip -o code.zip" % env.server_path)
    sudo("cd %s; rm -f code.zip" % env.server_path)
    local("rm -f code.zip")
    
    install_reqs()

def install_reqs():
    sudo('%s/pip install -r %s/requirements.txt' % (env.python_path, env.server_path))
    