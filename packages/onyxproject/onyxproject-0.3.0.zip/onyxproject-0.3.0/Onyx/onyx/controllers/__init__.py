# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, request, current_app, g, flash, url_for
from flask_login import login_required, logout_user
from onyxbabel import gettext as _
import os



core = Blueprint('core', __name__, url_prefix='/' , template_folder=os.path.dirname(os.path.dirname(__file__)) + '/templates')

from .views import *

