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
        if player.nationality == nat:
            players.append(player)

    print(f"Players from {nat}")
    print()
    players = sorted(players, key=lambda player: player.score, reverse = True)
    for player in players:
        print(player)
        
if __name__ == "__main__":
    main()
