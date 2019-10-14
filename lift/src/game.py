import os
from time import sleep
from flask import Blueprint, redirect
from flask import current_app as app


# TODO :
#
#   * Manage routes
#   * Manage templates

class Game:

    def __init__(self, name, startup, stop, is_running, tmux_name=""):
        """

        :param str name: should not have spaces or weird chars
        :param str tmux_name:
        :param list of str startup:
        :param stop:
        :param is_running:
        """
        self.name = name
        self.startup = startup
        self.stop = stop
        self.is_running = is_running
        self.game_blueprint = Blueprint(self.name, __name__)
        if tmux_name != "":
            self.tmux_name = tmux_name
        else:
            self.tmux_name = self.name

    def is_running(self):
        return os.system(self.is_running) == 0

    def has_tmux(self):
        return os.system("tmux has -t ={}".format(self.tmux_name)) == 0

    def send_to_tmux(self, command):
        os.system("""tmux send-keys -t {} {}""".format(self.tmux_name, command))

    def get_status(self):
        d = {}
        if self.has_tmux():
            d['tmux'.format(self.name)] = 'running'
        else:
            d['tmux'.format(self.name)] = 'stopped'
        if self.is_running():
            d['server'.format(self.name)] = 'running'
        else:
            d['server'.format(self.name)] = 'stopped'
            return d

    def start(self):
        # if no tmux with the name create one
        if not self.has_tmux():
            os.system("tmux new -d -s {}".format(self.tmux_name))
        if self.is_running():
            app.logger.info("{} server already running".format(self.name))
            return
        # start server
        for command in self.startup:
            # TODO we should add a way to input a bit of delay
            self.send_to_tmux(command)
        return

    def stop(self):
        # if no server running cannot operate
        if not self.is_running():
            app.logger.info("{} not running".format(self.name))
            return
        # if no tmux called server cannot operate
        if not self.has_tmux():
            app.logger.info("no tmux with correct name '{}'".format(self.tmux_name))
            return
        for command in self.stop:
            # TODO we should add a way to input a bit of delay
            self.send_to_tmux(command)
        return

    def restart(self):
        self.stop()
        while self.is_running():
            app.logger.info("Waiting for server to shutdown")
            sleep(1)
        self.start()
        return
