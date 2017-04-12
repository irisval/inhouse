from flask import render_template, redirect, request, flash
from flask_login import login_required, current_user
from . import web_module as mod_web
from . import controllers as controller
from application import CONFIG
from application import cache
from .models import *

@cache.cached()
@mod_web.route("/", methods=["GET", "POST"])
@mod_web.route('/')
def index():
	return render_template('web.index.html')