
In order to install the minimal analytics-experiments repository:

First, decide on your directories:
* VIRTUALENV_DIR = directory where you create your python virtualenv.
* BASE_DIR = directory you start in before cloning the analytics repo. (so something like /home/bob)
* DJANALYTICS_DIR = directory where the djanalytics repo is cloned. (so something like /home/bob/djanalytics/)
* EDXANALYTICS_DIR = directory where the edxanalytics repo is cloned (so something like /home/bob/edxanalytics/)

Then, start to install:
* cd BASE_DIR
* git clone git@github.com:MITx/djanalytics.git
* cd djanalytics (this is the DJANALYTICS_DIR)
* sudo xargs -a apt-packages.txt apt-get install
* sudo aptitude remove python-virtualenv python-pip
* sudo easy_install pip virtualenv
* pip install virtualenv
* mkdir VIRTUALENV_DIR
* virtualenv VIRTUALENV_DIR
* source VIRTUALENV_DIR/bin/activate
* python setup.py install
* cd BASE_DIR
* git clone git@github.com:edx/djeventstream.git
* cd djeventstream
* python manage.py install
* cd BASE_DIR
* git clone git@github.com:MITx/edxanalytics.git
* cd edxanalytics (this is the EDXANALYTICS_DIR)
* sudo xargs -a apt-packages.txt apt-get install
* pip install -r requirements.txt
* mkdir BASE_DIR/db
* cd EDXANALYTICS_DIR/src/edxanalytics
* Ensure that IMPORT_MITX_MODULES in edxanalytics/settings.py is False .
* python manage.py syncdb --database=remote --settings=edxanalytics.settings --settings=settings (this may fail, but that is fine)
* python manage.py syncdb --database=default --settings=edxanalytics.settings --settings=settings
* mkdir EDXANALYTICS_DIR/staticfiles
* python manage.py collectstatic --settings=settings --noinput -c --pythonpath=.

Then, run the server:
* python manage.py runserver 127.0.0.1:9022 --settings=edxanalytics.settings --pythonpath=. --nostatic
* Navigate to 127.0.0.1:9022 in your browser, and you should see a login screen.

Then, create a user:
* cd EDXANALYTICS_DIR/src/edxanalytics
* python manage.py shell --settings=edxanalytics.settings --pythonpath=.
* from django.contrib.auth.models import User (run in the shell)
* user = User.objects.create_user("test","test@test.com","test") (run in the shell)

If you are using the aws settings (ie deploying):

* MITX_DIR = directory where you clone MITX

* cd EDXANALYTICS_DIR/src/edxanalytics
* source VIRTUALENV_DIR/bin/activate
* python manage.py createcachetable django_cache --database=default --settings=edxanalytics.settings --pythonpath=.
* cd BASE_DIR
* git clone git@github.com:MITx/mitx.git
* cd MITX_DIR
* sudo xargs -a apt-packages.txt apt-get install
* If the above step does not work, remove npm and nodejs from apt-packages.txt
* pip install -r pre-requirements.txt
* pip install -r requirements.txt
* pip install webob
* pip install -r local-requirements.txt


Ignore
=====

Assorted notes; setting up a new machine with new edx/dj split. Below will turn into documentation

adduser pmitros
Create .ssh, and copy keys, set up sudoers

apt-get install emacs23 git python-pip python-matplotlib python-scipy mongodb apache2-utils python-mysqldb subversion ipython 
pip install django celery pymongo fs mako requests decorator South django-celery celery-with-redis

Nominally: 
pip install -e git+https://github.com/edx/djeventstream.git#egg=djeventstream

In practice, setup.py install

apt-get install nginx redis-server libmysqlclient-dev 
