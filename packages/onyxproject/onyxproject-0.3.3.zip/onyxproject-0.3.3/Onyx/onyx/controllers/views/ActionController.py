#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import core
from flask import redirect , url_for , request , g , jsonify , flash
from flask.ext.login import login_required
import json
from onyxbabel import gettext , lazy_gettext

@core.route('action/get/' , methods=['GET','POST'])
@login_required
def action():
	if request.method == 'POST':
		try:
			action = request.form['action']
			data = json.dumps(g.action)
			load = json.loads(data)
			url = load[action]['url']
			return redirect(url_for("core."+url))
		except:
			flash(gettext('An error has occurred !') , "error")
			return redirect(url_for("core.index"))

	flash(gettext('An error has occurred !') , "error")
	return redirect(url_for("core.index"))
