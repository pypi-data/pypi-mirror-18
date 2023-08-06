#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import core
from flask.ext.login import LoginManager , login_user , login_required , current_user , login_user , logout_user
from flask import request , render_template , redirect , url_for , flash , session
from onyxbabel import gettext
from ...models import *
from ...extensions import db , login_manager
from os.path import exists
import os
import hashlib


@login_manager.user_loader
def load_user(id):
    return UsersModel.User.query.get(int(id))
  
  
@core.route('register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('account/register.html')
    try:
        if request.form['password'] == request.form['verifpassword']:
            hashpass = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
            user = UsersModel.User(admin=0 , username=request.form['username'] , password=hashpass, email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            flash(gettext('Account Added !') , 'success')
            return redirect(url_for('core.hello'))
        else:
            flash(gettext('Passwords are not same !' ), 'error')
            return redirect(url_for('core.register'))
    except:
        db.session.rollback()
        if request.form['password'] == request.form['verifpassword']:
            hashpass = hashlib.sha1(request.form['password'].encode('utf-8')).hexdigest()
            user = UsersModel.User(admin=0 , username=request.form['username'] , password=hashpass, email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            flash(gettext('Account Added !') , 'success')
            return redirect(url_for('core.hello'))
        else:
            flash(gettext('Passwords are not same !' ), 'error')
            return redirect(url_for('core.register'))


@core.route('hello')
def hello():
    return render_template('account/hello.html')
 

@core.route('login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('account/login.html')
    try:
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        registered_user = UsersModel.User.query.filter_by(email=email,password=hashlib.sha1(password).hexdigest()).first()
        if registered_user is None:
            flash(gettext('Incorrect email or password !'), 'error')
            return redirect(url_for('core.login'))
        login_user(registered_user)
        registered_user.authenticated = True
        flash(gettext('You are now connected'), 'success')
        return redirect(request.args.get('next') or url_for('core.index'))
    except:
        flash(gettext('An error has occurred !'), 'error')
        return redirect(url_for('core.login'))


@core.route('account/delete' , methods=['GET','POST'])
@login_required
def accountdel():
    if request.method == 'GET':
        try:
            bdd = UsersModel.User.query.all()
            resultUsername = []
            for myusers in bdd:
                resultUsername.append(myusers.username) 
            resultUser = resultUsername

            resultEmailRow = []
            for myusers in bdd:
                resultEmailRow.append(myusers.email) 
            resultEmail = resultEmailRow

            resultIdRow = []
            for myusers in bdd:
                resultIdRow.append(myusers.id) 
            resultId = resultIdRow


            return render_template('account/delete.html' , username=resultUser , email=resultEmail , id=resultId )
        except:
            return render_template('account/delete.html' , error="Pas de comptes")


@core.route('account/delete/<id_delete>')
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
        return redirect(url_for('core.accountdel'))
    except:
        flash(gettext('An error has occurred !') , 'error')
        return redirect(url_for('core.accountdel'))


@core.route('account/manage' , methods=['GET','POST'])
@login_required
def accountManage():
    if request.method == 'GET':
        bdd = UsersModel.User.query.filter_by(username=current_user.username).first()
        buttonColor = bdd.buttonColor
        return render_template('account/manage.html' ,buttonColor=buttonColor )
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
            return redirect(url_for('core.accountManage'))
        else:
            flash(gettext('Passwords are not same !' ), 'error')
            return redirect(url_for('core.accountManage'))
    except:
        flash(gettext('Another user use data') , 'error')
        return redirect(url_for('core.accountManage'))

@core.route('account/manage/color' , methods=['GET','POST'])
@login_required
def changeColor():
    if request.method == 'GET':
        bdd = UsersModel.User.query.filter_by(username=current_user.username).first()
        buttonColor = bdd.buttonColor
        return render_template('account/color.html' ,buttonColor=buttonColor )
    try:
        user = UsersModel.User.query.filter_by(username=current_user.username).first()
        if not request.form['color']:
            user.buttonColor = current_user.buttonColor
        else:
            user.buttonColor = request.form['color']
        db.session.add(user)
        db.session.commit()
        flash(gettext('Account changed successfully') , 'success')
        return redirect(url_for('core.accountManage'))
    except:
        return redirect(url_for('core.accountManage'))



@core.route('logout' , methods=['GET','POST'])
def logout():
    login_manager.login_view = 'core.hello'
    logout_user()
    flash(gettext('You are now log out' ), 'info')
    return redirect(url_for('core.hello'))