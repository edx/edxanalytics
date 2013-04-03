"""
This fabfile currently works to deploy this repo and mitx to a new server.
A lot of settings and names will need to be changed around for your specific config, so
look through carefully.
"""

from __future__ import with_statement
from fabric.api import local, lcd, run, env, cd, settings, prefix, sudo, shell_env
from fabric.contrib.console import confirm
from fabric.operations import put
from fabric.contrib.files import exists

#Should be in the format user@remote_host
env.hosts = ['vik@prod-kpi-001.m.edx.org']
#Can set this to be a path to a local keyfile if nonstandard
#env.key_filename = ''

def prepare_deployment():
    #Make a local commit with latest changes if needed.
    local('git add -p && git commit')
    local("git push")

def deploy():
    #Setup needed directory paths
    #Edit if you are using this for deployment
    ea_dir = '/opt/wwc/edxanalytics'
    ea_src_dir = ea_dir + "/src/edxanalytics"
    dja_dir = '/opt/wwc/djanalytics'
    dje_dir = '/opt/wwc/djeventstream'
    mitx_code_dir = '/opt/wwc/mitx'
    up_one_level_dir = '/opt/wwc'
    database_dir = '/opt/wwc/db'
    remote_ssh_dir = '/home/vik/.ssh'
    local_dir = '/home/vik/mitx_all'
    static_dir = '/opt/wwc/staticfiles'
    virtualenv_dir = "/opt/edx"

    #this is needed for redis-server to function properly
    sudo('sysctl vm.overcommit_memory=1')
    #LCD defines the local directory
    with lcd(local_dir), settings(warn_only=True):
        #Cd defines the remote directory
        with cd(remote_ssh_dir):
            #Move local keys that can access github to remote host
            #Highly recommend that you use a password for these!
            put('service-id_rsa','id_rsa', use_sudo=True)
            put('service-id_rsa.pub','id_rsa.pub', use_sudo=True)
            #Change permissions on keyfile to ensure that it can be used
            sudo('chmod 400 id_rsa')

    with settings(warn_only=True):
        venv_exists = exists(virtualenv_dir, use_sudo=True)
        if not venv_exists:

        #Stop services
        sudo('service celery stop')
        sudo('service celery-xml stop')
        sudo('service celery-edge stop')
        sudo('service analytics stop')
        static_dir_exists = exists(static_dir, use_sudo=True)
        if not static_dir_exists:
            sudo('mkdir {0}'.format(static_dir))
        repo_exists = exists(ea_dir, use_sudo=True)
        #If the repo does not exist, then it needs to be cloned
        if not repo_exists:
            sudo('apt-get install git python')
            up_one_level_exists = exists(up_one_level_dir, use_sudo=True)
            if not up_one_level_exists:
                sudo('mkdir {0}'.format(up_one_level_dir))
            with cd(up_one_level_dir):
                #TODO: Insert repo name here
                run('git clone git@github.com:edx/djeventstream.git')
                run('git clone git@github.com:MITx/djanalytics.git')
                run('git clone git@github.com:MITx/edxanalytics.git')

        #Check for the existence of the mitx repo
        mitx_repo_exists = exists(mitx_code_dir, use_sudo=True)
        if not mitx_repo_exists:
            with cd(up_one_level_dir):
                run('git clone git@github.com:MITx/mitx.git')
        db_exists = exists(database_dir, use_sudo=True)
        if not db_exists:
            sudo('mkdir {0}'.format(database_dir))

        sudo('chown -R vik {0}'.format(up_one_level_dir))

    with cd(mitx_code_dir), settings(warn_only=True):
        #Update the mitx repo
        run('git pull')

    with cd(ea_dir), settings(warn_only=True):
        # With git...
        run('git pull')
        #Ensure that files are fixed
        run('sudo apt-get update')
        #This fixes an intermittent issue with compiling numpy
        run('sudo apt-get upgrade gcc')
        #Activate your virtualenv for python
        result = run('source /opt/edx/bin/activate')
        if result.failed:
            #If you cannot activate the virtualenv, one does not exist, so make it
            sudo('apt-get remove python-virtualenv python-pip')
            sudo('easy_install pip')
            run('pip install virtualenv')
            run('mkdir {0}'.format(virtualenv_dir))
            run('virtualenv {0}'.format(virtualenv_dir))
            sudo('chown -R vik {0}'.format(virtualenv_dir))

    with prefix('source /opt/edx/bin/activate'), settings(warn_only=True):
        with cd(dja_dir):
            sudo('xargs -a apt-packages.txt apt-get install')
            run('python setup.py install')

        with cd(dje_dir):
            run('python setup.py install')

        with cd(ea_dir):
            sudo('xargs -a apt-packages.txt apt-get install')
            run('pip install -r requirements.txt')

        with cd(ea_src_dir):
            # Sync django db and migrate it using south migrations
            run('python manage.py syncdb --database=remote --settings=edxdeployment.aws --pythonpath={0}'.format(ea_src_dir))
            run('python manage.py syncdb --database=default --settings=edxdeployment.aws --pythonpath={0}'.format(ea_src_dir))
            run('python manage.py migrate --database=default --settings=edxdeployment.aws --pythonpath={0}'.format(ea_src_dir))
            run('python manage.py collectstatic -c --noinput --settings=edxdeployment.aws --pythonpath={0}'.format(ea_src_dir))
            run('python manage.py createcachetable django_cache --database=default --settings=edxdeployment.aws --pythonpath={0}'.format(ea_src_dir))
        sudo('chown -R www-data {0}'.format(up_one_level_dir))

        with cd(mitx_code_dir):
            sudo('xargs -a apt-packages.txt apt-get install')
            run('pip install -r pre-requirements.txt')
            run('pip install -r requirements.txt')
            run('pip install webob')
            run('pip install -r local-requirements.txt')

    with lcd(local_dir), settings(warn_only=True):
        with cd(up_one_level_dir):
            #Move env and auth.json (read by aws.py if using it instead of settings)
            put('analytics-auth.json', 'auth.json', use_sudo=True)
            put('analytics-env.json', 'env.json', use_sudo=True)
            put('kpi-mitx-auth.json', 'kpi-mitx-auth.json', use_sudo=True)
            put('kpi-mitx-auth-xml.json', 'kpi-mitx-auth-xml.json', use_sudo=True)
        with cd('/etc/init'):
            #Upstart tasks that start and stop the needed services
            put('analytics-celery.conf', 'celery.conf', use_sudo=True)
            put('analytics-celery-xml.conf', 'celery-xml.conf', use_sudo=True)
            put('analytics-celery-edge.conf', 'celery-edge.conf', use_sudo=True)
            put('analytics.conf', 'analytics.conf', use_sudo=True)
        with cd('/etc/nginx/sites-available'):
            #Modify nginx settings to pass through ml-service-api
            put('analytics-nginx', 'default', use_sudo=True)

    #Start all services back up
    sudo('service celery start')
    sudo('service celery-xml start')
    sudo('service celery-edge start')
    sudo('service analytics start')
    sudo('service nginx restart')