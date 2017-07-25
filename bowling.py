class Player:
    def __init__(self, name):
        self.name = name
        self.points = []


players = []
players_count = int(input("How many players? "))

for i in range(players_count):
    players.append(Player(input("Enter name of " + str(i + 1) + " player: ")))

for player in players:
    print(player.name)