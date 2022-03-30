import os
import subprocess
from time import sleep

from flask import Blueprint, redirect, request
from flask import current_app as app
import requests

juk = Blueprint("juk", __name__)

status_ok = 'ok'
status_unreach = 'unreachable'
status_ukerr = 'unknown error'


def get_status():
    try:
        response = requests.get(app.config["JK_ADDRESS"]+"status")
    except ConnectionError as e:
        return status_unreach
    except:
        return status_ukerr
    return status_ok


@juk.route("/juk-start")
def start():
    # if get_status() != status_ok:
    #     subprocess.call("./start.sh", shell=True, cwd=app.config["JK_PATH"])
    #     sleep(1)
    return redirect("/jukebox")


@juk.route("/juk-stop")
def stop():
    if get_status() == status_ok:
        os.system("screen -XS Jukebox quit")
    return redirect("/jukebox")



@juk.route("/juk-restart")
def restart():
    # Restarting is essencially the same as starting it
    return start()
