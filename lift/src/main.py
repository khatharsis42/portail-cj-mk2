from flask import Flask, render_template, request, redirect, Blueprint
import logging

from src.game_manager import GameManager
from src.jukebox import juk
from src.jukebox import get_status as jukebox_status
from src.utils import url_name, get_inspiro

app = Flask(__name__, template_folder="../templates", static_folder="../static")

game_blueprint = Blueprint("game_manager_bp", __name__)
app.register_blueprint(game_blueprint)
app.register_blueprint(juk)

log=logging.getLogger('werkzeug')
log.setLevel(logging.INFO)


gameManager = GameManager()
gameManager.load_all()


@app.route("/")
def index():
    status=dict()
    jukebox_status()
    get_inspiro(status)
    current_tab = request.args.get("tab", "Liens", type=str)
    return render_template("accueil.html", status=status, url_name=url_name, current_tab=current_tab)


@app.route("/game/")
def list_games():
    status = dict()
    descriptions = dict()
    for game in gameManager.games.values():
        status[game.name] = game.get_status()
        descriptions[game.name] = game.description
    return render_template("game.html", games=gameManager.games.keys(), status=status, descriptions=descriptions)


@app.route("/game/start/<gamename>")
def route_game_start(gamename):
    """

    :return: Redirects to
    """
    game = gameManager.games[gamename]
    game.start()
    return redirect("/game")


@app.route("/game/stop/<gamename>")
def route_game_stop(gamename):
    game = gameManager.games[gamename]
    game.stop()
    return redirect("/game")


@app.route("/game/restart/<gamename>")
def route_game_restart(gamename):
    game = gameManager.games[gamename]
    game.restart()
    return redirect("/game")


@app.route("/game/reload/")
def route_game_reload():
    gameManager.reload_all()
    return redirect("/game")

