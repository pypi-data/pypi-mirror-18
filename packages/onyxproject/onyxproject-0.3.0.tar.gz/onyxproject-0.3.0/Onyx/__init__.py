#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Onyx
import os
import pip

try:
	os.rename(str(Onyx.__path__[0]) + "/onyx/config_example.py" , str(Onyx.__path__[0]) + "/onyx/config.py")
	print('Config File Create')
except:
	print('Config File Already Create')


from .onyx import create_app
from .onyx.extensions import db

def runserver():
	#Check Updates
	print("Check Update")
	pip.main(['install', '--upgrade' , "onyxproject"])
	app = create_app()
	try:
		app.run('0.0.0.0' , port=80 , debug=False)
	except:
		app.run('0.0.0.0' , port=8080 , debug=False)