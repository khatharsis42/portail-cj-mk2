import os
from time import sleep
from flask import Blueprint, redirect
from flask import current_app as app

mc = Blueprint("mc", __name__)

# searching for something like server.1.14.1.jar
def is_running():
    return os.system("""pgrep -f "^java.*server\..*\.jar nogui$" """)==0

def has_tmux():
    return os.system("tmux has -t =minecraft")==0

@mc.route("/mc-start")
def start():
    # if no tmux called minecraft create one
    if not has_tmux():
        os.system("tmux new -d -s minecraft")
    if is_running():
        app.logger.info("minecraft server already running")
        return redirect("/?tab=Minecraft")
    os.system("""tmux send-keys -t minecraft "mc-snap" ENTER""")
    return redirect("/?tab=Minecraft")

@mc.route("/mc-stop")
def stop():
    # if no server running cannot operate
    if not is_running():
        app.logger.info("minecraft not running")
        return redirect("/?tab=Minecraft")
    # if no tmux called minecraft cannot operate
    if not has_tmux():
        app.logger.info("no tmux with correct name 'minecraft'")
        return redirect("/?tab=Minecraft")
    os.system("""tmux send-keys -t minecraft "stop" ENTER""")
    return redirect("/?tab=Minecraft")

@mc.route("/mc-restart")
def restart():
    stop()
    while is_running():
        app.logger.info("Waiting for server to shutdown")
        sleep(1)
    start()
    return redirect("/?tab=Minecraft")
