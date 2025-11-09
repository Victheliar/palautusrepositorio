import requests
from player import Player
from rich.prompt import Prompt
from rich.align import Align
from rich.console import Console
from rich.table import Table


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
    
    def top_scores_by_nationality(self, nationality, season):
            self.players = [player for player in self.players if player.nationality==nationality]
            self.players = sorted(self.players, key=lambda player: player.score, reverse = True)
            table = Table(title=f"Season {season} players from {nationality}")
            table.add_column("Name", justify="left", style="cyan", no_wrap=True)
            table.add_column("teams", style="magenta")
            table.add_column("goals",justify="right",style="green")
            table.add_column("assists",justify="right",style="green")
            table.add_column("points",justify="right",style="green")
            for player in self.players:
                table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.score))
            console = Console()
            console.print(table)  

def main():
    seasons = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
    season = Prompt.ask("Season", choices=seasons ,default="2024-2025")
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    nationalities = ["USA", "FIN", "CAN", "SWE", "CZE", "RUS", "SLO", "FRA", "GBR", "SVK", "DEN", "NED", "AUT", "BLR", "GER", "SUI", "NOR", "UZB", "LAT", "AUS"]
    nationality = Prompt.ask("Nationality", choices = nationalities, case_sensitive = False)
    players = stats.top_scores_by_nationality(nationality, season)      
        
if __name__ == "__main__":
    main()
