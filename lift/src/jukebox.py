import os
from time import sleep
from flask import Blueprint, redirect, request
from flask import current_app as app
from src.utils import url_name
import urllib.request, urllib.error

juk = Blueprint("juk", __name__)

status_ok = 'ok'
status_unreach = 'unreachable'
status_ukerr = 'unknown error'


def has_tmux():
    return os.system("tmux has -t =jukebox") == 0


def get_status():
    d = dict()
    if (has_tmux()):
        d['juk_tmux'] = 'running'
    else:
        d['juk_tmux'] = 'stopped'

    try:
        response = urllib.request.urlopen("http://jukebox.cj")
    except urllib.error.URLError:
        d['juk_server'] = status_unreach
    except:
        d['juk_server'] = status_ukerr
    else:
        d['juk_server'] = status_ok
    return d


@juk.route("/juk-start")
def start():
    # if no tmux called minecraft create one
    if not has_tmux():
        os.system("tmux new -d -s jukebox")
    if get_status()['juk_server'] == status_ok:
        # return message : the jukebox is already running
        return redirect("/?tab=Jukebox")
    os.system("""tmux send-keys -t jukebox "cd {}" ENTER""".format(app.config["JK_PATH"]))
    os.system("""tmux send-keys -t jukebox "python3 run.py" ENTER""")
    return redirect("/?tab=Jukebox")


@juk.route("/juk-stop")
def stop():
    # if not running cannot operate
    status = get_status()
    if status['juk_server'] == status_unreach:
        app.logger.info("Jukebox is not up")
        return redirect("/?tab=Jukebox")
    # if no tmux called jukebox cannot operate
    if not status["juk_tmux"]:
        app.logger.info("No tmux with correct name 'jukebox'")
        return redirect("/?tab=Jukebox")
    os.system("""tmux send-keys -t jukebox C-c""")
    return redirect("/?tab=Jukebox")


@juk.route("/juk-restart")
def restart():
    stop()
    while get_status['juk_server'] == status_ok:
        app.logger.info("Waiting for jukebox to shutdown")
        sleep(1)
    start()
    return redirect("/?tab=Jukebox")
