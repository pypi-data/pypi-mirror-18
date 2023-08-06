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
			tasks.append(e)
		return render_template('task.html' , tasks=tasks)

@core.route('task/add' , methods=['GET','POST'])
@login_required
def addTask():
	if request.method == 'POST':
		text = request.form['content']
		task = TaskModel.Task(idAccount=str(current_user.id),text=text)
		db.session.add(task)
		db.session.commit()
		return json.dumps({'status':'success','id':task.id})

@core.route('task/delete' , methods=['GET','POST'])
@login_required
def deleteTask():
	if request.method == 'POST':
		delete = TaskModel.Task.query.filter_by(id=request.form['id'],idAccount=str(current_user.id)).first()
		db.session.delete(delete)
		db.session.commit()
		return redirect(url_for('core.task'))