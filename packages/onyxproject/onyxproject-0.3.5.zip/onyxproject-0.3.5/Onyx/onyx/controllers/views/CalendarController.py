#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request , redirect , url_for , jsonify
from flask.ext.login import login_required , current_user
from .. import core
from ...models import *
from ...extensions import db
import os
import json
import string





@core.route('calendrier' , methods=['GET','POST'])
@login_required
def calendar():
	if request.method == 'GET':
		events = []
		bdd = CalendarModel.Calendar.query.filter(CalendarModel.Calendar.idAccount.endswith(str(current_user.id)))

		for fetch in bdd:	
			e = {}
			e['id'] = fetch.id
			e['title'] = fetch.title
			e['notes'] = fetch.notes
			e['lieu'] = fetch.lieu
			e['start'] = fetch.start
			e['end'] = fetch.end
			e['color'] = fetch.color
			events.append(e)
		
		return render_template('calendar/view.html' , events=events)
	update = CalendarModel.Calendar.query.filter_by(id=request.form['id'],idAccount=str(current_user.id)).first()
	update.start = request.form['start']
	update.end = request.form['end']
	db.session.add(update)
	db.session.commit()
	return json.dumps({'status':'success'})

@core.route('calendar/set/add' , methods=['GET','POST'])
@login_required
def addCalendar():
	if request.method == 'POST':
		color = request.form['color']
		enddate = request.form['end']
		startdate = request.form['start']
		title = request.form['title']
		notes = request.form['notes']
		lieu = request.form['lieu']
		calendar = CalendarModel.Calendar(idAccount=str(current_user.id),title=title , notes=notes , lieu=lieu , start=startdate, end=enddate ,color=color)
		db.session.add(calendar)
		db.session.commit()
		return redirect(url_for('core.calendar'))

@core.route('calendar/set/editTitle' , methods=['GET','POST'])
@login_required
def editEventTitle():
	if request.method == 'POST':
		checked = 'delete' in request.form
		if checked == True:
			delete = CalendarModel.Calendar.query.filter_by(id=request.form['id'],idAccount=str(current_user.id)).first()
			db.session.delete(delete)
			db.session.commit()
			return redirect(url_for('core.calendar'))
		update = CalendarModel.Calendar.query.filter_by(id=request.form['id'],idAccount=str(current_user.id)).first()
		update.title = request.form['title']
		update.notes = request.form['notes']
		update.lieu = request.form['lieu']
		update.color = request.form['color']
		db.session.add(update)
		db.session.commit()
		return redirect(url_for('core.calendar'))

@core.context_processor
def utility_processor():
    def split(str):
        return str.split(" ")
    return dict(split=split)

	
