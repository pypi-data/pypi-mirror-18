# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, request, current_app, g, flash, url_for
from flask.ext.login import LoginManager , login_user , login_required , current_user , login_user , logout_user
from flask_babel import gettext as _
from ..extensions import db , login_manager
from ..models import *
import os
import site
import hashlib
import os.path
import datetime



install = Blueprint('install', __name__, url_prefix='/install', template_folder=os.path.dirname(os.path.dirname(__file__)) + '/templates')


@login_manager.user_loader
def load_user(id):
    return UsersModel.User.query.get(int(id))


@install.route('/' , methods=['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('install/index.html')
	db.session.rollback()
	hashpass = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
	user = UsersModel.User(admin=1 ,confirmed_on=datetime.datetime.now(),registered_on=datetime.datetime.now(),confirmed=True, username=request.form['username'] , password=hashpass, email=request.form['email'])
	db.session.add(user)
	db.session.commit()
	login_user(user)
	try:
		os.rename(os.path.dirname(os.path.dirname(__file__)) + '/install', os.path.dirname(os.path.dirname(__file__)) + '/installOld')
	except:
		import Onyx
		os.rename(str(Onyx.__path__[0]) + "/onyx/install" , str(Onyx.__path__[0]) + "/onyx/installOld")
	flash('Onyx a bien été installé !' , 'success')
	return redirect(url_for("install.finish"))


@install.route('/finish' , methods=['GET','POST'])
@login_required
def finish():
	return render_template('install/finish.html')
