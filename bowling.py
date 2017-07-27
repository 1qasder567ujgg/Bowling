class Player:
    def __init__(self, name):
        self.name = name
        self.points = []


def getNumberOfPlayers():
    while True:
        try:
            pl_cnt = int(input("How many players? Up to 5. 0 to exit "))
            if 0 <= pl_cnt <= 5:
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

def setScreen(players):
    print("\033[2J", end="")
    print("\033[H", end="")
    print("\033[3B", end="")

    i = 1
    for player in players:
        print("\033[1B", end="")
        print('Player #' + str(i) + ': ' + player.name)
        #print("\033[1A", end="")
        #print(' __'*21)
        print('|__' * 21 + '|')
        print('|_____' * 9 + '|________|')
        i += 1

def showScore(player, order, round):
    score_up = ''
    score_down = ''
    for p in player.points:
        score1 = '_' + str(p[0])
        score2 = '_' + str(p[1])
        score_up += '|' + score1[-2:] + '|' + score2[-2:]
        score1 = '__' + str(p[2]) + '__'
        score_down += '|' + score1[:5] 

    print("\033[H", end="")
    print("\033[" + str(5 + 4*(order-1)) + "B", end="")
    print(score_up, end='')
    print("\033[1B", end="")
    print("\033[" + str(7 + 4*(order-1)) + ";1H", end="")
    print(score_down, end='')



NUMBER_OF_ROUNDS = 3

#Clear screen & move to the top
print("\033[2J", end="")
print("\033[H", end="")

players_count = getNumberOfPlayers()
if players_count != 0:
    players = getPlayers(players_count)

    setScreen(players)
    print("\033[H", end="")

    for i in range(NUMBER_OF_ROUNDS):
        p = 1
        for player in players:
            score_msg = 'Round #' + str(i + 1) + ': ' + player.name
            print("\033[H", end="")
            print("\033[2K", end="")
            first_trow = int(input(score_msg + ", what is your 1st score? "))
            if first_trow == 10:
                player.points.append([first_trow, 0, "X"])
                showScore(player, p, i)
            else:
                print("\033[H", end="")
                print("\033[2K", end="")
                second_throw =  int(input(score_msg + ", what is your 2nd score? "))
                if first_trow + second_throw == 10:
                    player.points.append([first_trow, second_throw, "/"])
                    showScore(player, p, i)
                else:
                    player.points.append([first_trow, second_throw, first_trow + second_throw])
                    showScore(player, p, i)
            p += 1

print("\033[3B", end="\r")