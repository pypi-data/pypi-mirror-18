#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request , redirect , url_for
from flask.ext.login import login_required , current_user
from .. import core
from ...models import *
from ...extensions import db
import os
import json

@core.route('task' , methods=['GET','POST'])
@login_required
def task():
	if request.method == 'GET':
		tasks = []
		bdd = TaskModel.Task.query.filter(TaskModel.Task.idAccount.endswith(str(current_user.id)))
		for fetch in bdd:	
			e = {}
			e['id'] = fetch.id
			e['text'] = fetch.text
			e['date'] = fetch.date
			e['idCalendar'] = fetch.idCalendar
			tasks.append(e)
		return render_template('task.html' , tasks=tasks)

@core.route('task/add' , methods=['GET','POST'])
@login_required
def addTask():
	if request.method == 'POST':
		text = request.form['text']	
		if not request.form['date']:
			task = TaskModel.Task(idAccount=str(current_user.id),text=text)
			db.session.add(task)
			db.session.commit()
			return json.dumps({'status':'success','calendar':'false','id':task.id})
		else:
			date = request.form['date'] + " 00:00:00"
			if request.form['calendar'] == "1":		
				
				calendar = CalendarModel.Calendar(idAccount=str(current_user.id), title=text , notes=text , start=date, end=date )
				db.session.add(calendar)
				db.session.commit()
				task = TaskModel.Task(idAccount=str(current_user.id),text=text,date=date , idCalendar=calendar.id)
				db.session.add(task)
				db.session.commit()
				return json.dumps({'status':'success','calendar':'true','id':task.id,'idCalendar':calendar.id})
			else:
				task = TaskModel.Task(idAccount=str(current_user.id),text=text,date=date)
				db.session.add(task)
				db.session.commit()
				return json.dumps({'status':'success','calendar':'false','id':task.id})
		

@core.route('task/delete' , methods=['GET','POST'])
@login_required
def deleteTask():
	if request.method == 'POST':
		if request.form['idCalendar'] == "false":
			delete = TaskModel.Task.query.filter_by(id=request.form['id'],idAccount=str(current_user.id)).first()
			db.session.delete(delete)
			db.session.commit()
		else:
			delete = TaskModel.Task.query.filter_by(id=request.form['id'],idAccount=str(current_user.id)).first()
			db.session.delete(delete)
			db.session.commit()
			deleteCalendar = CalendarModel.Calendar.query.filter_by(id=request.form['idCalendar'],idAccount=str(current_user.id)).first()
			db.session.delete(deleteCalendar)
			db.session.commit()
		return redirect(url_for('core.task'))
	
@core.context_processor
def utility_processor():
	def split(str):
		pre = str.split(" ")
		return pre
	return dict(split=split)