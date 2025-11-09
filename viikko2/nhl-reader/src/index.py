import requests
from player import Player

def main(nat='FIN'):
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    # print("JSON-muotoinen vastaus:")
    # print(response)

    players = []

    for player_dict in response:
        player = Player(player_dict)
        players.append(player)

    print(f"Players from {nat}")

    for player in players:
        if player.nationality == nat:
            print(player)
        
if __name__ == "__main__":
    main(nat)
