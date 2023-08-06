#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import core
from flask import render_template , request
from flask.ext.login import login_required
import wikipedia



@core.route('wiki', methods=['GET', 'POST'])
@login_required
def wiki():
    if request.method == 'GET':
    	return render_template('wiki/index.html')
    try:
    	wikipedia.set_lang("fr")
    	article = wikipedia.page(request.form['search'])
    	return render_template('wiki/result.html', head = article.title , url =article.url , summary=wikipedia.summary(request.form['search']))
    except:
    	return render_template('wiki/result.html', head = "Erreur" , summary="Ce que vous avez recherché n'existe pas sur wikipedia fr !")