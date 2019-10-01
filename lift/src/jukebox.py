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
    return os.system("tmux has -t =jukebox")==0

def get_status():
    try:
        response = urllib.request.urlopen("http://jukebox.cj")
    except urllib.error.URLError:
        return status_unreach
    except:
        return status_ukerr
    else:
        return status_ok


@juk.route("/juk-start")
def start():
    # if no tmux called minecraft create one
    if not has_tmux():
        os.system("tmux new -d -s jukebox")
    if get_status() ==status_ok:
        # return message : the jukebox is already running
        return redirect("/?tab=Jukebox")
    #os.system("""tmux send-keys -t jukebox C-c "cd /home/membre/soft/jukebox-ultra-nrv/" ENTER""")
    os.system("""tmux send-keys -t jukebox C-c "cd /home/membre/Documents/prog/python/jukebox-ultra-nrv/" ENTER""")
    os.system("""tmux send-keys -t jukebox "python3 run.py" ENTER""")
    return redirect("/?tab=Jukebox")

@juk.route("/juk-stop")
def stop():
    # if not running cannot operate
    if get_status()== status_unreach:
        app.logger.info("Jukebox is not up")
        return redirect("/?tab=Jukebox")
    # if no tmux called jukebox cannot operate
    if not has_tmux():
        app.logger.info("No tmux with correct name 'jukebox'")
        return redirect("/?tab=Jukebox")
    os.system("""tmux send-keys -t jukebox C-c""")
    return redirect("/?tab=Jukebox")

@juk.route("/juk-restart")
def restart():
    stop()
    while get_status()==status_ok:
        app.logger.info("Waiting for jukebox to shutdown")
        sleep(1)
    start()
    return redirect("/?tab=Jukebox")
