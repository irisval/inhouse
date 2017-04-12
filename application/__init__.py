from flask import Flask, redirect, flash, render_template
from mongoengine import register_connection
import jinja2
from flask_cache import Cache

# Credits for Jinja overloading method:
# http://fewstreet.com/2015/01/16/flask-blueprint-templates.html
class FlaskApp(Flask):
    def __init__(self):
        Flask.__init__(self, __name__)
        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            jinja2.PrefixLoader({}, delimiter = ".")
        ])
    def create_global_jinja_loader(self):
        return self.jinja_loader

    def register_blueprint(self, blueprint):
        Flask.register_blueprint(self, blueprint)
        self.jinja_loader.loaders[1].mapping[blueprint.name] = blueprint.jinja_loader

app = FlaskApp()
app.config.from_pyfile("../config.cfg")
CONFIG = app.config

# MongoLab
register_connection(
    alias = "default", 
    name = CONFIG["DB_NAME"],
    username = CONFIG["DB_USERNAME"],
    password = CONFIG["DB_PASSWORD"],
    host = CONFIG["DB_HOST"],
    port = CONFIG["DB_PORT"]
)

#Cache
cache = Cache(app, config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": 60 * 60 * 24 * 7})

@app.errorhandler(401)
def error(e):
    return redirect("/login?next="+request.path)

@app.errorhandler(403)
def error(e):
    flash("You do not have permission to view that page.", "error")
    return redirect("/")

@app.errorhandler(404)
def error(e):
    return render_template("404.html"), 404

@app.errorhandler(410)
def error(e):
    return render_template("410.html"), 410

@app.errorhandler(500)
def error(e):
    return render_template("500.html"), 500

@app.errorhandler(502)
def error(e):
    return render_template("502.html"), 502

# from application.mod_web import web_module
# app.register_blueprint(web_module)
# from application.mod_hacker import hacker_module
# app.register_blueprint(hacker_module)
# from application.mod_user import user_module
# app.register_blueprint(user_module)
# from application.mod_admin import admin_module
# app.register_blueprint(admin_module)
# from application.mod_stats import stats_module
# app.register_blueprint(stats_module)
