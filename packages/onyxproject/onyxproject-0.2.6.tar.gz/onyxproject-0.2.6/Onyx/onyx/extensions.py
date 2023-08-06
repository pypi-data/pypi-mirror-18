# -*- coding: utf-8 -*-


from flask_mail import Mail
mail = Mail()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_flatpages import FlatPages
pages = FlatPages()

import flask_restless
manager = flask_restless.APIManager()

from flask_login import LoginManager
login_manager = LoginManager()
try:
	login_manager.login_view = 'core.hello'
except:
	login_manager.login_view = 'install.installer'

import Onyx
from flask_babelex import Babel , Domain
domain = Domain(domain=str(Onyx.__path__[0]) + "/onyx/translations")
babel = Babel()

from flask_migrate import Migrate
migrate = Migrate()

from flask_wtf.csrf import CsrfProtect
csrf = CsrfProtect()

from flask_cache import Cache
cache = Cache()

from celery import Celery
celery = Celery()


