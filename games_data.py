import pandas as pd

class GamesData:
    def __init__(self):
        # Dane z wynikami meczów
        self.games_raw = pd.read_csv('European Tour - wyniki.csv', sep=';') # Surowy plik z meczami, bez powtórek
        self.games_doubled = None # Plik z meczami, który zawiera duble

        # Dane ogólne na temat cyklu
        self.players = None # Lista graczy
        self.events = None # Lista eventów
        self.unique_events_list = None # Lista eventów z latami (unikatowe)
        self.ovr_games_count = None # Ogólna liczba meczów
        self.ovr_average = None # Średnia całego cyklu

        self.create_games_doubled()
        self.load_overall_data()

    def create_games_doubled(self):
        self.games_doubled = self.games_raw.copy()
        self.games_doubled['Zawodnik'] = self.games_raw['Przeciwnik']
        self.games_doubled['Przeciwnik'] = self.games_raw['Zawodnik']
        self.games_doubled['AVG - zawodnik'] = self.games_raw['AVG - przeciwnik']
        self.games_doubled['AVG - przeciwnik'] = self.games_raw['AVG - zawodnik']
        self.games_doubled['Wynik'] = self.games_doubled['Wynik'].apply(lambda x: ';'.join(reversed(x.split(';'))))

        self.games_raw['LP'] = self.games_raw['LP'] * 2 - 1
        self.games_raw.index = self.games_raw['LP']
        self.games_raw = self.games_raw.drop(columns=['LP'], axis=1)
        self.games_raw = self.games_raw.sort_index()
        self.games_raw['Wynik'] = self.games_raw['Wynik'].str.replace(';', ':')
        self.games_raw['AVG - zawodnik'] = self.games_raw['AVG - zawodnik'].fillna('')
        self.games_raw['AVG - przeciwnik'] = self.games_raw['AVG - przeciwnik'].fillna('')
        self.games_raw['Data'] = pd.to_datetime(self.games_raw['Data'], format='%d.%m.%Y')
        self.games_raw['Data'] = self.games_raw['Data'].dt.strftime('%d/%m/%Y')

        self.games_doubled['LP'] = self.games_doubled['LP'] * 2
        self.games_doubled.index = self.games_doubled['LP']
        self.games_doubled = self.games_doubled.drop(columns=['LP'], axis=1)
        self.games_doubled['Wynik'] = self.games_doubled['Wynik'].str.replace(';', ':')
        self.games_doubled['AVG - zawodnik'] = self.games_doubled['AVG - zawodnik'].fillna('')
        self.games_doubled['AVG - przeciwnik'] = self.games_doubled['AVG - przeciwnik'].fillna('')
        self.games_doubled['Data'] = pd.to_datetime(self.games_doubled['Data'], format='%d.%m.%Y')
        self.games_doubled['Data'] = self.games_doubled['Data'].dt.strftime('%d/%m/%Y')

        self.games_doubled = pd.concat([self.games_raw, self.games_doubled])

    def load_overall_data(self):
        self.players = self.games_raw['Zawodnik'].tolist()
        self.players = list(set(self.players))
        self.players.sort()

        self.events = self.games_raw['Turniej'].tolist()
        self.events = list(set(self.events))
        self.events.sort()

        self.unique_events_list = self.games_raw[['Data', 'Turniej']]
        self.unique_events_list['Data'] = self.unique_events_list['Data'].astype(str).str[-4:]
        self.unique_events_list['Turniej'] = self.unique_events_list['Data'] + " " + self.unique_events_list['Turniej']
        self.unique_events_list = self.unique_events_list.drop(columns=['Data'])
        self.unique_events_list = self.unique_events_list['Turniej'].tolist()
        self.unique_events_list = list(set(self.unique_events_list))
        self.unique_events_list.sort()

        self.ovr_games_count = len(self.games_raw)

        list_of_averages = list(self.games_doubled['AVG - zawodnik'])
        list_of_averages = [avg for avg in list_of_averages if avg != '']
        self.ovr_average = round(sum(list_of_averages) / len(list_of_averages), 2)

        return {
            "unique_events_count": len(self.unique_events_list),
            "games_count": self.ovr_games_count,
            "wins_count": "---",
            "titles_count": "---",
            "average": self.ovr_average
        }

    def load_players_data(self, player):
        player_unique_events_list = self.games_doubled[self.games_doubled['Zawodnik'] == player][['Data', 'Turniej']]
        player_unique_events_list['Data'] = player_unique_events_list['Data'].astype(str).str[-4:]
        player_unique_events_list['Turniej'] = player_unique_events_list['Data'] + " " + player_unique_events_list['Turniej']
        player_unique_events_list = player_unique_events_list.drop(columns=['Data'])
        player_unique_events_list = player_unique_events_list['Turniej'].tolist()
        player_unique_events_list = (list(set(player_unique_events_list)))

        player_games_count = int(self.games_doubled['Zawodnik'].value_counts()[player])
        player_wins_count = int(self.games_raw['Zawodnik'].value_counts()[player])
        player_titles_count = int(len(self.games_raw[(self.games_raw['Zawodnik'] == player) & (self.games_raw['Faza'] == 'Final')]))

        player_avg = list(self.games_doubled[self.games_doubled['Zawodnik'] == player]['AVG - zawodnik'])
        player_avg = [avg for avg in player_avg if avg != '']
        player_avg = round(sum(player_avg) / len(player_avg), 2)

        print(player_wins_count)

        return {
            "unique_events_count": len(player_unique_events_list),
            "games_count": player_games_count,
            "wins_count": player_wins_count,
            "titles_count": player_titles_count,
            "average": player_avg
        }