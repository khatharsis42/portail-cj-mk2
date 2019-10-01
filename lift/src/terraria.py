import os
from time import sleep
from flask import Blueprint, redirect
from flask import current_app as app

mc = Blueprint("mc", __name__)
tmux_name = "terraria"

# searching for something like server.1.14.1.jar
def is_running():
    # TODO
    return os.system("""pgrep "^TerrariaServer$" """)==0

def has_tmux():
    return os.system("tmux has -t ={}".format(tmux_name))==0

@mc.route("/terraria-start")
def start():
    # if no tmux called terraria create one
    if not has_tmux():
        os.system("tmux new -d -s {}".format(tmux_name))
    if is_running():
        app.logger.info("terraria server already running")
        return redirect("/?tab=Terraria")
    os.system("""tmux send-keys -t {} "terraria-server" ENTER""".format(tmux_name))
    return redirect("/?tab=Terraria")

@mc.route("/terraria-stop")
def stop():
    # if no server running cannot operate
    if not is_running():
        app.logger.info("terraria not running")
        return redirect("/?tab=Terraria")
    # if no tmux called terraria cannot operate
    if not has_tmux():
        app.logger.info("no tmux with correct name '{}'".format(tmux_name))
        return redirert("/?tab=Terraria")
    os.system("""tmux send-keys -t terraria "stop" ENTER""")
    return redirect("/?tab=Terraria")

@mc.route("/terraria-restart")
def restart():
    stop()
    while is_running():
        app.logger.info("Waiting for server to shutdown")
        sleep(1)
    start()
    return redirect("/?tab=Terraria")