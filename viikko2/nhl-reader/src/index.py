import requests
from player import Player

class PlayerReader:
    def __init__(self, url):
        self.url = url
        self.players = []
    
    def get_players(self):
        response = requests.get(self.url).json()
        for player_dict in response:
            player = Player(player_dict)
            self.players.append(player)
        return self.players

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader
        self.players = reader.get_players()
    
    def top_scores_by_nationality(self, nationality):
            print(f"Players from {nationality}")
            print()
            self.players = [player for player in self.players if player.nationality==nationality]
            return sorted(self.players, key=lambda player: player.score, reverse = True)


def main(nat='FIN'):
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scores_by_nationality("FIN")
    for player in players:
        print(player)
        
if __name__ == "__main__":
    main()
