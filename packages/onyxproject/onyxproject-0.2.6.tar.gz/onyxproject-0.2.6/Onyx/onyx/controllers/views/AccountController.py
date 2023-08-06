#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import core
from flask.ext.login import LoginManager , login_user , login_required , current_user , login_user , logout_user
from flask import request , render_template , redirect , url_for , flash , session
from flask.ext.babelex import gettext
from flask.ext.mail import Message
from ...models import *
from ...extensions import db , mail , login_manager
from ...config import SECRET_KEY
from ...config import SECURITY_PASSWORD_SALT
from os.path import exists
import hashlib
import datetime
from itsdangerous import URLSafeTimedSerializer
import os




def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email



def send_mail(recipient , title , message):
    msg = Message(title, sender = 'Onyx', recipients = [recipient])
    msg.html = message
    mail.send(msg)

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
            user = UsersModel.User(admin=0 ,confirmed_on=datetime.datetime.now(),registered_on=datetime.datetime.now(),confirmed=False, username=request.form['username'] , password=hashpass, email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            token = generate_confirmation_token(request.form['email'])
            confirm_url = url_for('core.confirm_email', token=token, _external=True)
            html = render_template('account/activate.html', confirm_url=confirm_url)
            subject = "Confirmer votre compte Onyx"
            send_mail(request.form['email'], subject, html)
            login_user(user)
            flash(gettext('A mail will be send to your mail address'), 'success')
            return redirect(url_for('core.unconfirmed'))        
        else:
            flash(gettext('Passwords are not same !' ), 'error')
            return redirect(url_for('core.register'))
    except:
        flash(gettext('You name or password are already used !' ), 'error')
        return redirect(url_for('core.hello'))

@core.route('register/resetpassword' , methods=['GET','POST'])
def resetpassword():
    if request.method == 'GET':
        return render_template('account/reset.html' , mail=True)
    try:
        token = generate_confirmation_token(request.form['email'])
        confirm_url = url_for('core.confirm_reset', token=token, _external=True)
        html = render_template('account/resetMail.html', confirm_url=confirm_url)
        subject = "Changer votre mot de passe Onyx"
        send_mail(request.form['email'], subject, html)
        flash(gettext('A mail will be send to your mail address'), 'success')
        return redirect(url_for('core.resetpassword'))
    except:
        flash(gettext("We don't know your mail" ), 'error')
        return redirect(url_for('core.resetpassword'))


@core.route('register/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash(gettext('The link is invalid or expire'), 'error')
    user = UsersModel.User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash(gettext('You can now connect'), 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(gettext('Your account is active now'), 'success')
    return redirect(url_for('core.index'))


@core.route('register/resetpassword/confirm/<token>', methods=['GET','POST'])
def confirm_reset(token):
    if request.method == 'GET':
        try:
            email = confirm_token(token)
        except:
            flash(gettext('The link is invalid or expire'), 'error')
        user = UsersModel.User.query.filter_by(email=email).first_or_404()
        return render_template('account/resetPassword.html')
    try:
        email = confirm_token(token)
        user = UsersModel.User.query.filter_by(email=email).first()
        user.password = hashlib.sha1(request.form['password']).hexdigest()
        db.session.add(user)
        db.session.commit()
        flash(gettext('Password changed !' ), 'success')
        return redirect(url_for('core.hello'))
    except:
        flash(gettext('An error has occurred !') , 'error')
        return redirect(url_for('core.hello'))



@core.route('unconfirmed')
def unconfirmed():
    flash(gettext('Please confirm your account !'), 'error')
    return render_template('account/unconfirmed.html')

@core.route('resend' , methods=['GET' , 'POST'])
def resend_confirmation():
    if request.method == 'GET':
        return render_template('account/resend.html')
    try:
        token = generate_confirmation_token(request.form['email'])
        confirm_url = url_for('core.confirm_email', token=token, _external=True)
        html = render_template('account/activate.html', confirm_url=confirm_url)
        subject = "Veuillez confirmer votre adresse mail !"
        send_mail(request.form['email'], subject, html)
        flash(gettext('A new mail will be send !'), 'success')
        return redirect(url_for('core.unconfirmed'))
    except:
        flash(gettext("You can't watch it !"), 'success')
        return redirect(url_for('core.index'))



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
        if registered_user.confirmed:
            login_user(registered_user)
            registered_user.authenticated = True
            flash(gettext('You are now connected'), 'success')
            return redirect(request.args.get('next') or url_for('core.index'))
        else:
            return redirect(url_for('core.unconfirmed'))
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