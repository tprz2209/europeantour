from flask import render_template, request, jsonify
from games_data import GamesData

data = GamesData()

class WebProcessor:
    def __init__(self):
        self.games_raw = data.games_raw
        self.games_doubled = data.games_doubled

        self.players_with_all_option = None

    def generate_search_list(self):
        self.players_with_all_option = data.players.copy()
        self.players_with_all_option.insert(0, "Wszystko")
        return self.players_with_all_option

    def send_games_to_js(self):
        if request.args.get('name') == "Wszystko":
            player_data = self.games_raw
            player_stats = data.load_overall_data()
        else:
            player_name = request.args.get('name')
            player_data = self.games_doubled.loc[self.games_doubled['Zawodnik'] == player_name]
            player_stats = data.load_players_data(player_name)

        player_info = player_data.to_dict(orient="index")
        player_info = [player_info, player_stats]
        return player_info