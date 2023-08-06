#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request , redirect , url_for
from flask.ext.login import login_required
from .. import core
import os


@core.route('help')
@login_required
def help():
    return render_template('help.html')
