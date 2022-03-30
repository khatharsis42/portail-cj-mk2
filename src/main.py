from flask import Flask, render_template, request, redirect, Blueprint
import logging

from src.game_manager import GameManager
from src.jukebox import juk, get_status
from src.utils import get_inspiro

app = Flask(__name__, template_folder="../templates", static_folder="../static")

game_blueprint = Blueprint("game_manager_bp", __name__)
app.register_blueprint(game_blueprint)
app.register_blueprint(juk)

log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

gameManager = GameManager()
gameManager.load_all()


@app.route("/")
def index():
    return render_template("accueil.html")


@app.route("/Canvas")
def canvas():
    return render_template("canvas.html")


@app.route('/Liens')
def links():
    return render_template("liens.html",
                           jukebox_address=app.config["JK_ADDRESS"],
                           canvas_address=app.config["CV_ADDRESS"],
                           bdd_address=app.config["BDD_ADDRESS"],)


@app.route("/Jukebox")
def jukebox():
    return render_template("jukebox.html",
                           status=get_status(),
                           jukebox_address=app.config["JK_ADDRESS"],
                           )


@app.route("/Inspirobot")
def inspirobot():
    return render_template("inspirobot.html",
                           status=get_inspiro(),
                           )


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
