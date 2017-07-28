class Player:
    def __init__(self, name):
        self.name = name
        self.points = []


def exitBowling(clearScreen=False):
    if clearScreen:
        print("\033[2J", end="")
        print("\033[H", end="")        
    else:
        print("\033[1A", end="\r")
        print("\033[K", end="")
    exit(0)


def getNumberOfPlayers():
    while True:
        try:
            pl_cnt = int(input("How many players? (Up to 5) "))
            if 0 <= pl_cnt <= 5:
                break
        except KeyboardInterrupt:
            exitBowling()
        except:
            pass
        print("\033[1A", end="")
        print("\033[K", end="")
    return pl_cnt


def getPlayers(pl_cnt):
    p = []
    for i in range(pl_cnt):
        while True:
            try:
                p_name = input("Player #" + str(i + 1) + " name: ").strip()
                if len(p_name) != 0:
                    break
            except KeyboardInterrupt:
                exitBowling(True)
            except:
                pass
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
        print('|__' * 21 + '|')
        print('|_____' * 9 + '|________|')
        i += 1


def showUpperScore(score, throw, turn, order):
    score = '__' + str(score)
    print("\033[H", end="")
    print("\033[" + str(6    + 4*(order-1)) + ';' + str(2 + 6*turn + 3*(throw - 1)) + "H", end="")
    print(score[-2:], end='')


def showLowerScore(player, order):
    score_down = ''
    for i, p in enumerate(player.points):
        score_down += '|__' 
        if i == 9:
            score_down += '_'
        score_down += str(p[3]) + '_'
        if len(str(p[3])) == 1:
            score_down += '_'

    print("\033[1B", end="")
    print("\033[" + str(7 + 4*(order-1)) + ";1H", end="")
    print(score_down, end='')


def showtotalScore(score, throw, turn, order):
    score = '__' + str(score)
    print("\033[H", end="")
    print("\033[" + str(6 + 4*(order-1)) + ';' + str(2 + 6*turn + 3*(throw - 1)) + "H", end="")
    print(score[-2:], end='')


def getThrow(msg, last_throw, is_last):

    print("\033[H", end="")
    print("\033[2K", end="")
    
    while True:
        try:
            score = int(input(msg))
            if ((0 <= score + last_throw <= 10) and not is_last) or ((0 <= score <= 10) and is_last):
                break
        except KeyboardInterrupt:
            exitBowling()
        except:
            pass
        print("\033[1A", end="")
        print("\033[K", end="")

    return score


NUMBER_OF_ROUNDS = 10

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
            first_trow = getThrow(score_msg + ", what is your 1st score? ", 0, False)
            showUpperScore(first_trow, 1, i, p)
            if i > 0:
                if player.points[-1][3] == 'X':
                    if i > 1:
                        if player.points[-2][3] == 'X' and len(player.points) > 1:
                            player.points[-2][3] = 20 + first_trow

            if i > 0:
                if player.points[-1][3] == '/' and player.points:
                    player.points[-1][3] = 10 + first_trow

            showLowerScore(player, p)

            if first_trow == 10 and i < 9:
                player.points.append([first_trow, 0, 0, "X"])
                showLowerScore(player, p)
            else:
                if i == 9:
                    is_last = True
                else:
                    is_last = False
                second_throw = getThrow(score_msg + ", what is your 2nd score? ", first_trow, is_last)
                showUpperScore(second_throw, 2, i, p)

                if i > 0:
                    if player.points[-1][3] == 'X' and player.points:
                        player.points[-1][3] = 10 + first_trow + second_throw
                
                showLowerScore(player, p)
                
                if i < 9:
                    if first_trow + second_throw == 10:
                        player.points.append([first_trow, second_throw, 0, "/"])
                        showLowerScore(player, p)
                    else:
                        player.points.append([first_trow, second_throw, 0, first_trow + second_throw])
                        showLowerScore(player, p)
                else:
                    if first_trow == 10 or (first_trow + second_throw == 10):
                        tird_throw = getThrow(score_msg + ", what is your 3rd score? ", second_throw, True)
                        showUpperScore(tird_throw, 3, i, p)
                        player.points.append([first_trow, second_throw, tird_throw, first_trow + second_throw + tird_throw])
                    else:
                        player.points.append([first_trow, second_throw, '', first_trow + second_throw])
                    showLowerScore(player, p)
                    
            p += 1

print("\033[3B", end="\r")