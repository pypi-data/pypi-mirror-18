# -*- coding: utf-8 -*-
#pylint:disable-msg=W0612

import os
from flask import Flask, request, render_template , g , abort , redirect , url_for
from celery import Celery
from .extensions import (db, mail, pages, manager, login_manager, babel, csrf, cache, celery)
from flask_login import current_user
import os.path
from os.path import dirname, abspath, join
import json
from onyxbabel import gettext , lazy_gettext



# blueprints
try:
    from .install import install
    BLUEPRINTS = install
    blueprint_name = 'install'
except:
    from .controllers import core
    from .plugins import plugins
    from .auth import auth
    from .api import api_v1
    BLUEPRINTS = [core,auth,api_v1,plugins]
    blueprint_name = 'core'

__all__ = ('create_app', 'create_celery', )




def create_app(config=None, app_name='onyx', blueprints=None):
    app = Flask(app_name,
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
        template_folder= 'templates'
    )    
    try:
        app.config.from_object('Onyx.onyx.config')
    except:
        app.config.from_object('onyx.config')
    app.config.from_pyfile('../local.cfg', silent=True)
    if config:
        app.config.from_pyfile(config)

    if blueprints is None:
        blueprints = BLUEPRINTS

    blueprints_fabrics(app, blueprints)
    extensions_fabrics(app)

    error_pages(app , blueprint_name)
    gvars(app)

    with app.app_context():
        from migrate.versioning import api
        db.create_all()
        try:
            if not os.path.exists(app.config['SQLALCHEMY_MIGRATE_REPO']):
                api.create(app.config['SQLALCHEMY_MIGRATE_REPO'], 'database repository')
                api.version_control(app.config['SQLALCHEMY_DATABASE_URI'],app.config['SQLALCHEMY_MIGRATE_REPO'])
            else:
                api.version_control(app.config['SQLALCHEMY_DATABASE_URI'], app.config['SQLALCHEMY_MIGRATE_REPO'],
                                    api.version(app.config['SQLALCHEMY_MIGRATE_REPO']))
        except:
            print("Migrate Already Done")
        print ("Base de donnee initialisee")
  
    return app
  

  



def create_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

def blueprints_fabrics(app, blueprints):
    """Configure blueprints in views."""
    try:
        for blueprint in blueprints:
            app.register_blueprint(blueprint)
    except:
        app.register_blueprint(blueprints)


def extensions_fabrics(app):
    db.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    pages.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    celery.config_from_object(app.config)
    


def gvars(app):
  
  
    @app.before_request
    def gvariables():
        g.user = current_user
        g.gapi = app.config.get('GAPI')
        g.gcx = app.config.get('GCX')
        g.action = { gettext('Quel temps fait il ?'): { "id" : "0" , "type" : "url" , "url" : "weather" }, gettext('Weather'): { "id" : "1" , "type" : "url" , "url" : "weather" } }
                

    @app.context_processor
    def inject_user():
        try:
            return {'user': g.user}
        except AttributeError:
            return {'user': None}

    @app.teardown_request
    def teardown_request(exception):
        if exception:
            db.session.rollback()
            db.session.remove()
        db.session.remove()



    @babel.localeselector
    def get_locale():
        if g.user:
            if hasattr(g.user, 'lang'):
                return g.user.lang
        accept_languages = app.config.get('ACCEPT_LANGUAGES')
        return request.accept_languages.best_match(accept_languages)


def error_pages(app , name):
    # HTTP error pages definitions

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("404.html", blueprint=name), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html" , blueprint=name), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template("404.html", blueprint=name), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("404html", blueprint=name), 500

