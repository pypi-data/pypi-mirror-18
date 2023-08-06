#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request , redirect , url_for
from .. import core
import os

@core.route('info')
def info():
    return render_template('info.html')