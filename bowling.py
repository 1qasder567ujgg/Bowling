class Player:
    def __init__(self, name):
        self.name = name
        self.points = []


def getNumberOfPlayers():
    while True:
        try:
            pl_cnt = int(input("How many players? "))
            break
        except:
            print("\033[1A", end="")
            print("\033[K", end="")
    return pl_cnt


FRAMES = 3
players = []

#Clear screen & move to the top
print("\033[2J", end="")
print("\033[H", end="")

players_count = getNumberOfPlayers()

for i in range(players_count):
    players.append(Player(input("Enter name of " + str(i + 1) + " player: ")))

for i in range(FRAMES):
    for player in players:
    #     print(player.name)

        first_trow = int(input(player.name + ", what is your 1st score? "))
        if first_trow == 10:
            player.points.append([first_trow, 0, "X"])
        else:
            second_throw =  int(input(player.name + ", what is your 2nd score? "))
            if first_trow + second_throw == 10:
                player.points.append([first_trow, second_throw, "/"])
            else:
                player.points.append([first_trow, second_throw, first_trow + second_throw])
        print(player.name, player.points)

for player in players:
    print(player.name, player.points)
