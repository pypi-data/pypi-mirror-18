#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request , redirect , url_for
from flask.ext.login import login_required
from .. import core
import os

@core.route('tv')
@login_required
def tv():
	return render_template('tv/index.html')
