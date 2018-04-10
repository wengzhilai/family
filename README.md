microblog
=========

A decently featured microblogging web application written in Python and Flask that I'm developing in my Flask Mega-Tutorial series that begins [here](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

Installation
------------

The tutorial referenced above explains how to setup a virtual environment with all the required modules. As a convenience, the `setup.py` script will create this virtual environment for you. You can run this script again to refresh any missing modules.

The sqlite database must also be created before the application can run, and the `db_create.py` script takes care of that. See the [Database tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database) for the details.

Running
-------

pip3 install virtualenv

export PATH=$PATH/:/Library/Frameworks/Python.framework/Versions/3.6/bin

virtualenv -p python3 --no-site-packages venv
virtualenv --no-site-packages venv

To run the application in the development web server just execute `run.py` with the Python interpreter from the flask virtual environment.

python -m venv flask

pip install flask
pip install flask-login
pip install flask-openid
pip install flask-mail
pip install flask-sqlalchemy
pip install sqlalchemy-migrate
pip install flask-whooshalchemy
pip install flask-wtf
pip install flask-babel
pip install guess_language
pip install flipflop
pip install coverage

pip install pymssql
pip install PyMySQL
pip3 install -U flask-cors
pip3 install flask-httpauth
git remote remove origin
git remote add origin https://github.com/wengzhilai/family

https://github.com/	wengzhilai	wengzhilai123


pip install mysql-python
source /home/soft/flask-sqlacodegen/venv/bin/activate
deactivate
python ./sqlacodegen/main.py --noviews --noindexes --flask --outfile ~/github/family/app/entity/model.py mysql://FA:abcdef123@47.254.16.126:3306/fa


/private/var/root/Desktop/Family/family/venv/Scripts/
