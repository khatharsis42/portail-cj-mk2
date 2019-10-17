import json
import os

from flask import current_app as app

from src.game import Game


class GameManager:

    def __init__(self):
        """

        """
        self.games = dict()
        self.game_directory = "gamelist/"

    def reload_all(self):
        self.games = dict()
        self.load_all()

    def load_all(self):
        for f in os.listdir(self.game_directory):

            # app.logger.info("in for {}".format(f))
            # if f.is_dir(os.join(self.game_directory, f)):
            # app.logger.info("Loading configuration {}".format(f))
            print(f)
            gamename = os.path.splitext(f)[0]
            self.load_game(gamename)

    def load_game(self, gamename):
        """

        :param string gamename: the name of the game to load
        :return:
        """
        with open(self.game_directory + gamename + ".json", 'r') as f:
            json_game = f.read()
        json_game = json.loads(json_game)
        assert json_game["name"] == gamename
        try:
            tmux_name = json_game["name"]
        except KeyError:
            tmux_name = ""
        try:
            description = json_game["description"]
        except KeyError:
            description = ""
        self.games[json_game["name"]] = Game(
            json_game["name"],
            json_game["start"],
            json_game["stop"],
            json_game["is_running"],
            tmux_name=tmux_name,
            description=description
        )
