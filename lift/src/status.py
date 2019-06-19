from src.minecraft import is_running
from src.minecraft import has_tmux as mc_tmux
from src.jukebox import get_status
from src.jukebox import has_tmux as juk_tmux

# add minecraft related statuses to the dict d
def minecraft_status(d):
    if (mc_tmux()):
        d['mc_tmux']='running'
    else:
        d['mc_tmux']='stopped'
    if (is_running()):
        d['mc_server']='running'
    else:
        d['mc_server']='stopped'

def jukebox_status(d):
    if (juk_tmux()):
        d['juk_tmux']='running'
    else:
        d['juk_tmux']='stopped'
    d['juk_get']=get_status()
