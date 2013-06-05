sudo adduser --disabled-password --gecos "" pmitros
sudo cp -dpr secure/ssh ~pmitros/.ssh
sudo chown -R pmitros:pmitros ~pmitros/.ssh

cd ~/skeleton
sudo apt-get update
# These are copied out of the repos. 
# This guarantees we have things like git, but 
# we'll want to repeat with the latest versions too. 
export DEBIAN_FRONTEND=noninteractive
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password password ""'
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password_again password ""'
cat deploy-apt-packages.txt | sudo xargs apt-get -y install
cat dj-apt-packages.txt | sudo xargs apt-get -y install
cat edx-apt-packages.txt | sudo xargs apt-get -y install
cat mitx-apt-packages.txt | sudo xargs apt-get -y install
sudo easy_install -U distribute

sudo mkdir -p /opt/wwc
sudo chown pmitros:pmitros /opt/wwc

sudo pip install wsgi

cd /opt/wwc
sudo su pmitros -c "git clone git@github.com:edx/loghandlersplus.git"
cd /opt/wwc/loghandlersplus
sudo python setup.py install
cd /opt/wwc
sudo su pmitros -c "git clone git@github.com:edx/djeventstream.git"
cd /opt/wwc/djeventstream
sudo python setup.py install
cd /opt/wwc
sudo su pmitros -c "git clone git@github.com:edx/djanalytics.git"
cd /opt/wwc/djanalytics
sudo pip install -r requirements.txt 
sudo python setup.py install
cd /opt/wwc/mitx
# sudo pip install -r pre-requirements.txt -- Use system numpy, and we got distribute before
sudo su pmitros -c "grep -v scipy requirements.txt  > req_no_scipy.txt"
sudo pip install -r req_no_scipy.txt
sudo pip install -r repo-requirements.txt

cd /opt/wwc

sudo su pmitros -c "git clone git@github.com:edx/edxanalytics.git"
sudo su pmitros -c "git clone git@github.com:edx/mitx.git"
cd /opt/wwc/edxanalytics/src/edxanalytics
echo no | sudo su pmitros -c "python manage.py syncdb"
sudo su pmitros -c "python manage.py migrate"

cd ~/skeleton
sudo cp ~/skeleton/init/* /etc/init/
sudo cp ~/skeleton/sudoers.d/* /etc/sudoers.d/
sudo cp nginx/nginx.passwd /etc/nginx/nginx.passwd
sudo cp nginx/sites-enabled/* /etc/nginx/sites-enabled

sudo cp ~/secure/*json /opt/wwc

sudo service nginx restart
sudo service analytics start


# sudo su pmitros -c virtualenv python
# source python/bin/activate

# BASE=/opt/wwc
# PYTHON_DIR="$BASE/python"
# RUBY_DIR="$BASE/ruby"
# RUBY_VER="1.9.3"

# rvm install $RUBY_VER --with-readline
