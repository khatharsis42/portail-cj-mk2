import os
from flask import Blueprint, redirect
from flask import current_app as app
from lift.src.game import Game

minecraft_blueprint = Blueprint("minecraft", __name__)


minecraft = Game("minecraft",
                         [
                             """tmux send-keys -t minecraft "mc-snap" ENTER"""
                         ],
                         [
                             """tmux send-keys -t minecraft "stop" ENTER"""
                         ],
                         """pgrep -f "^java.*server\..*\.jar nogui$" """
                         )


@minecraft_blueprint.route("/game/minecraft-start")
def route_start():
    minecraft.start()
    return redirect("/?tab=Minecraft")


@minecraft_blueprint.route("/game/minecraft-stop")
def route_stop():
    # if no server running cannot operate
    if not minecraft.is_running():
        app.logger.info("minecraft not running")
        return redirect("/?tab=Minecraft")
    # if no tmux called minecraft cannot operate
    if not minecraft.has_tmux():
        app.logger.info("no tmux with correct name 'minecraft'")
        return redirect("/?tab=Minecraft")
    os.system("""tmux send-keys -t minecraft "stop" ENTER""")
    return redirect("/?tab=Minecraft")


@minecraft_blueprint.route("/game/minecraft-restart")
def route_restart():
    minecraft.restart()
    return redirect("/?tab=Minecraft")
