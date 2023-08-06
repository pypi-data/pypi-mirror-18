# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, request, current_app, g, flash, url_for
from flask_login import login_required, logout_user
from onyxbabel import gettext as _
from ..extensions import db


auth = Blueprint('auth', __name__, url_prefix='/auth/', template_folder="templates")
