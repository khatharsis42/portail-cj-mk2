import os
from src.minecraft import is_running, has_tmux
import urllib.request, urllib.error

def url_name(current_url):
    return current_url.split(':')[0]

# add minecraft related statuses to the dict d
def minecraft_status(d):
    if (has_tmux()):
        d['mc_tmux']='running'
    else:
        d['mc_tmux']='stopped'
    if (is_running()):
        d['mc_server']='running'
    else:
        d['mc_server']='stopped'

def jukebox_status(d):
    if os.system("tmux has -t =jukebox")==0:
        d['juk_tmux']='running'
    else:
        d['juk_tmux']='stopped'
    d['juk_get']='unknown'
    try:
        #TODO : url is fixed but would be great to take it dynamically
        response = urllib.request.urlopen("http://"+"192.168.98.20"+":8080/status")
    except urllib.error.URLError:
        d['juk_get']='unreachable'
    except:
        d['juk_get']='unknown error'
    else:
        d['juk_get']='ok'
