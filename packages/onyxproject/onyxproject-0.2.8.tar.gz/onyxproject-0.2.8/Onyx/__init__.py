#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Onyx
import os

try:
	os.rename(str(Onyx.__path__[0]) + "/onyx/config_example.py" , str(Onyx.__path__[0]) + "/onyx/config.py")
	print('Config File Create')
except:
	print('Config File Already Create')


from .onyx import create_app
from .onyx.extensions import db

def runserver():
	app = create_app()
	app.run(debug=True)