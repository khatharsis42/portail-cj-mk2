from flask import Flask, render_template
from src.minecraft import mc
from src.status import *
import logging

app = Flask(__name__, template_folder="../templates", static_folder="../static")

app.register_blueprint(mc)

log=logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

@app.route("/")
def index():
    status=dict()
    minecraft_status(status)
    jukebox_status(status)
    return render_template("accueil.html", status=status, url_name=url_name)
