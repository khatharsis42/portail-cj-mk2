from flask import Flask, render_template, request
from src.minecraft import mc
from src.jukebox import juk
from src.status import *
from src.utils import url_name, get_inspiro
import logging

app = Flask(__name__, template_folder="../templates", static_folder="../static")

app.register_blueprint(mc)
app.register_blueprint(juk)

log=logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

@app.route("/")
def index():
    status=dict()
    minecraft_status(status)
    jukebox_status(status)
    get_inspiro(status)
    current_tab = request.args.get("tab", "Liens", type=str)
    return render_template("accueil.html", status=status, url_name=url_name, current_tab=current_tab)
