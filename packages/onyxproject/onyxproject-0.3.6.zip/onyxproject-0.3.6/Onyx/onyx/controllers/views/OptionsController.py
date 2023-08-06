#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import core
from ...extensions import db
from flask import render_template , redirect , url_for , flash , request
from flask.ext.login import login_required , current_user
from onyxbabel import gettext
from ...models import *
from ...extensions import db
from ...decorators import admin_required
import platform
import pip
import os


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@core.route('options' , methods=['GET','POST'])
@login_required
def options():
	if request.method == 'GET':
		return render_template('options/index.html')
	try:
		user = UsersModel.User.query.filter_by(username=current_user.username).first()
		if not request.form['color']:
			user.buttonColor = current_user.buttonColor
		else:
			user.buttonColor = request.form['color']
		if not request.form['lang']:
			user.lang = current_user.lang
		else:
			user.lang = request.form['lang']
		db.session.add(user)
		db.session.commit()
		flash(gettext('Account changed successfully' ), 'success')
		return redirect(url_for('core.options'))
	except:
		flash(gettext("You don't enter param"), 'success')
		return redirect(url_for('core.options'))
		

@core.route('shutdown')
@admin_required
@login_required
def shutdown():
    shutdown_server()
    return render_template('options/close.html')

@core.route('maj')
@admin_required
@login_required
def maj():
	try:
		pip.main(['install', '--upgrade' , "onyxproject"])
		from ...config import SQLALCHEMY_DATABASE_URI
		from ...config import SQLALCHEMY_MIGRATE_REPO
		import imp
		from migrate.versioning import api
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
		tmp_module = imp.new_module('old_model')
		old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		exec(old_model, tmp_module.__dict__)
		script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,SQLALCHEMY_MIGRATE_REPO,tmp_module.meta, db.metadata)
		open(migration, "wt").write(script)
		api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
		print('New migration saved as ' + migration)
		print('Current database version: ' + str(v))
		flash(gettext("Onyx is now upgrade !"),'success')
		return redirect(url_for('core.options'))
	except:
		flash(gettext("An error has occured !"), 'error')
		return redirect(url_for('core.options'))