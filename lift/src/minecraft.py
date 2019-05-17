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

@mc.route("/launch-server")
def launch():
    # if no tmux called minecraft create one
    if not has_tmux():
        os.system("tmux new -d -s minecraft")
    if is_running():
        # return message : the server is already running
        return redirect("/minecraft-running")
    os.system("""tmux send-keys -t minecraft "mc-snap" ENTER""")
    return redirect("/after-launch")

@mc.route("/stop-server")
def stop():
    # if no server running cannot operate
    if not is_running():
        # return message : no server running
        return redirect("/no-minecraft")
    # if no tmux called minecraft cannot operate
    if not has_tmux():
        # return message : no tmux with correct name
        return redirect("/no-tmux")
    os.system("""tmux send-keys -t minecraft "stop" ENTER""")
    return redirect("/after-stop")

@mc.route("/restart-server")
def restart():
    stop()
    debug=True
    #while is_running():
    while (debug):
        debug_result = os.system("""pgrep -f "^java.*server\..*\.jar nogui$" """)
        print("found : ", debug_result)
        debug = (debug_result == 0)
        sleep(1)
    launch()
    return redirect("/after-restart")
