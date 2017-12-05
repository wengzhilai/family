#!/usr/bin/python
import os, subprocess, sys
#subprocess.call(['python3:', 'virtualenv.py', 'flask'])
#if sys.platform == 'win32':
#    bin = 'Scripts'
#else:
subprocess.call(['pip3', 'install', 'flask'])
subprocess.call(['pip3', 'install', 'flask-login'])
subprocess.call(['pip3', 'install', 'flask-openid'])
subprocess.call(['pip3', 'install', 'flask-mail'])
subprocess.call(['pip3', 'install', 'sqlalchemy'])
subprocess.call(['pip3', 'install', 'flask-sqlalchemy'])
subprocess.call(['pip3', 'install', 'sqlalchemy-migrate'])
subprocess.call(['pip3', 'install', 'flask-whooshalchemy'])
subprocess.call(['pip3', 'install', 'flask-wtf'])
subprocess.call(['pip3', 'install', 'flask-babel'])
subprocess.call(['pip3', 'install', 'flask-cors'])
subprocess.call(['pip3', 'install', 'Flask-HTTPAuth'])
subprocess.call(['pip3', 'install', 'flup'])
