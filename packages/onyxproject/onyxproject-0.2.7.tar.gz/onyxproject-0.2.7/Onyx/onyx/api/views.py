# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, current_app


from flask_restplus import Api

from .controllers import *

apikey = "dada"

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(version='1.0',title="Onyx API",description="Onyx Api version 1.0",)
api.init_app(api_v1)
api.add_namespace(calendar.api)
api.add_namespace(users.api)
api.add_namespace(tasks.api)


