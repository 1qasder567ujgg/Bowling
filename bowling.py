class Player:
    def __init__(self, name):
        self.name = name
        self.points = []


def getNumberOfPlayers():
    while True:
        try:
            pl_cnt = int(input("How many players? (Up to 5) "))
            if 0 < pl_cnt < 6:
                break
        except:
            pass
        print("\033[1A", end="")
        print("\033[K", end="")
    return pl_cnt


def getPlayers(pl_cnt):
    p = []
    for i in range(pl_cnt):
        while True:
            p_name = input("Player #" + str(i + 1) + " name: ").strip()
            if len(p_name) != 0:
                break
            print("\033[1A", end="")
            print("\033[K", end="")
        p.append(Player(p_name))
    return p


NUMBER_OF_ROUNDS = 3

#Clear screen & move to the top
print("\033[2J", end="")
print("\033[H", end="")

players_count = getNumberOfPlayers()
players = getPlayers(players_count)

for i in range(NUMBER_OF_ROUNDS):
    for player in players:

        first_trow = int(input(player.name + ", what is your 1st score? "))
        if first_trow == 10:
            player.points.append([first_trow, 0, "X"])
        else:
            second_throw =  int(input(player.name + ", what is your 2nd score? "))
            if first_trow + second_throw == 10:
                player.points.append([first_trow, second_throw, "/"])
            else:
                player.points.append([first_trow, second_throw, first_trow + second_throw])
        #print(player.name, player.points)

for player in players:
    print(player.name, player.points)
