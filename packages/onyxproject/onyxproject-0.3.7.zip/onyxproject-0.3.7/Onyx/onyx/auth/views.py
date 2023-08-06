# -*- coding: utf-8 -*-

from flask.ext.login import LoginManager , login_user , login_required , current_user , login_user , logout_user
from flask import request , render_template , redirect , url_for , flash , session , Blueprint, current_app, g
from onyxbabel import gettext
from ..models import *
from ..extensions import db , login_manager
from ..decorators import admin_required
from os.path import exists
import os
import hashlib
from ..assets import getAvatar
auth = Blueprint('auth', __name__, url_prefix='/auth/', template_folder="templates")


@auth.context_processor
def ButtonColor():
	try:
		buttonColor = current_user.buttonColor
	except:
		buttonColor = ""
	return dict(buttonColor=buttonColor)

@auth.context_processor
def currentAdmin():
	try:
		currentAdmin = current_user.admin
	except:
		currentAdmin = "Admin"
	return dict(currentAdmin=currentAdmin)

@auth.context_processor
def currentUser():
	try:
		currentUser = current_user.username
	except:
		currentUser = "User"
	return dict(currentUser=currentUser)

@auth.context_processor
def currentEmail():
	try:
		currentEmail = current_user.email
	except:
		currentEmail = "Email"
	return dict(currentEmail=currentEmail)

@auth.context_processor
def gravatar():
	def urlPicAvatar(id):
		return getAvatar.getAvatarById(id)
	return dict(urlPicAvatar=urlPicAvatar)


@login_manager.user_loader
def load_user(id):
    return UsersModel.User.query.get(int(id))
  
  
@auth.route('register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    try:
        if request.form['password'] == request.form['verifpassword']:
            hashpass = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
            user = UsersModel.User(admin=0 , username=request.form['username'] , password=hashpass, email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            flash(gettext('Account Added !') , 'success')
            return redirect(url_for('auth.hello'))
        else:
            flash(gettext('Passwords are not same !' ), 'error')
            return redirect(url_for('auth.register'))
    except:
        db.session.rollback()
        if request.form['password'] == request.form['verifpassword']:
            hashpass = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
            user = UsersModel.User(admin=0 , username=request.form['username'] , password=hashpass, email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            flash(gettext('Account Added !') , 'success')
            return redirect(url_for('auth.hello'))
        else:
            flash(gettext('Passwords are not same !' ), 'error')
            return redirect(url_for('auth.register'))


@auth.route('hello')
def hello():
    return render_template('hello.html')
 

@auth.route('login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    try:
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        registered_user = UsersModel.User.query.filter_by(email=email,password=hashlib.sha1(password).hexdigest()).first()
        if registered_user is None:
            flash(gettext('Incorrect email or password !'), 'error')
            return redirect(url_for('auth.login'))
        login_user(registered_user)
        registered_user.authenticated = True
        flash(gettext('You are now connected'), 'success')
        return redirect(request.args.get('next') or url_for('core.index'))
    except:
        flash(gettext('An error has occurred !'), 'error')
        return redirect(url_for('auth.login'))


@auth.route('account/delete' , methods=['GET','POST'])
@admin_required
@login_required
def accountdel():
    if request.method == 'GET':
        try:
            bdd = UsersModel.User.query.all()
      
            resultIdRow = []
            for myusers in bdd:
                resultIdRow.append(myusers) 
            resultId = resultIdRow


            return render_template('delete.html' , id=resultId )
        except:
            return render_template('delete.html' , error="Pas de comptes")


@auth.route('account/delete/<id_delete>')
@admin_required
@login_required
def delete_account(id_delete):
    try:
        delete = UsersModel.User.query.filter_by(id=id_delete).first()
        db.session.delete(delete)
        db.session.commit()
        deleteCalendar = CalendarModel.Calendar.query.filter(CalendarModel.Calendar.idAccount.endswith(str(id_delete)))
        for fetch in deleteCalendar:
            deleteEvent = CalendarModel.Calendar.query.filter_by(id=fetch.id).first()
            db.session.delete(deleteEvent)
            db.session.commit()
        deleteTask = TaskModel.Task.query.filter(TaskModel.Task.idAccount.endswith(str(id_delete)))
        for fetch in deleteTask:
            deleteEventTask = TaskModel.Task.query.filter_by(id=fetch.id).first()
            db.session.delete(deleteEventTask)
            db.session.commit()
        flash(gettext('Account deleted !') , 'success')
        return redirect(url_for('auth.accountdel'))
    except:
        flash(gettext('An error has occurred !') , 'error')
        return redirect(url_for('auth.accountdel'))
			
@auth.route('account/change/<id>', methods=['GET','POST'])
@admin_required
@login_required
def change_account(id):
	if request.method == 'GET':
		user = UsersModel.User.query.filter_by(id=id).first()
		return render_template('change.html', username=user.username,email=user.email)
	try:
		user = UsersModel.User.query.filter_by(id=id).first()
		if not request.form['username']:
			user.username = user.username
		else:
			user.username = request.form['username']
		if not request.form['email']:
			user.email = user.email
		else:
			user.email = request.form['email']
		if not request.form['password']:
			user.password = user.password
		else:
			user.password = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
		db.session.add(user)
		db.session.commit()
		flash(gettext('Account changed !') , 'success')
		return redirect(url_for('auth.accountdel'))
	except:
		flash(gettext('An error has occurred !') , 'error')
		return redirect(url_for('auth.accountdel'))


@auth.route('account/manage' , methods=['GET','POST'])
@login_required
def accountManage():
    if request.method == 'GET':
        bdd = UsersModel.User.query.filter_by(username=current_user.username).first()
        buttonColor = bdd.buttonColor
        return render_template('manage.html' ,buttonColor=buttonColor )
    try:
        user = UsersModel.User.query.filter_by(username=current_user.username).first()
        lastpassword = user.password
        if hashlib.sha1(request.form['lastpassword'].encode('utf-8')).hexdigest() == lastpassword:
            if not request.form['username']:
                user.username = current_user.username
            else:
                user.username = request.form['username']
            if not request.form['email']:
                user.email = current_user.email
            else:
                user.email = request.form['email']
            if not request.form['password']:
                user.password = current_user.password
            else:
                user.password = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
            db.session.add(user)
            db.session.commit()
            flash(gettext('Account changed successfully' ), 'success')
            return redirect(url_for('auth.accountManage'))
        else:
            flash(gettext('Passwords are not same !' ), 'error')
            return redirect(url_for('auth.accountManage'))
    except:
        flash(gettext('Another user use data') , 'error')
        return redirect(url_for('auth.accountManage'))


@auth.route('logout' , methods=['GET','POST'])
@login_required
def logout():
    login_manager.login_view = 'auth.hello'
    logout_user()
    flash(gettext('You are now log out' ), 'info')
    return redirect(url_for('auth.hello'))