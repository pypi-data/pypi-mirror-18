#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import json

from flask_script import Manager , Server
from flask_migrate import MigrateCommand
try:
    from Onyx import create_app
    from Onyx.extensions import db
except:
    from .onyx import create_app
    from .onyx.extensions import db

manager = Manager(create_app)


def runserver():
	app = create_app()
	app.run(debug=True)
    #manager.run()


if __name__ == "__main__":
    manager.run()
