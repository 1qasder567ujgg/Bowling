class Player:
    #Class for bowling players
    #name - name of a player
    #points - earned points
    def __init__(self, name):
        self.name = name
        self.points = []


def moveHome():
    #Move the cursor to the top left corner
    print("\033[H", end="")        

def clearScreen():
    #Clear everything
    print("\033[2J", end="")
    moveHome()


def cleanLine():
    #Clean current line
    print("\033[2K", end="")


def moveByLine(direction, numberOfLines):
    #Move the cursor up or down by specified number of lines
    #Direction: A - up
    #           B - down
    print("\033[" + str(numberOfLines) + direction, end="")


def moveXY(line, column):
    #Move the cursor to the specified position:
    #Line - line number
    #Column - column number
    print("\033[" + str(line) + ";" + str(column) + "H", end="")


def moveUpAndClean():
    #Move one line up and clean it
    moveByLine('A', 1)
    cleanLine()


def exitBowling(clearAll=False):
    #Set the screen before exiting the program
    if clearAll:
        #Clear everything
        clearScreen()
    else:
        #Leave score
        moveUpAndClean()
    exit(0)


def getNumberOfPlayers():
    #Get number of players
    #Input value should be an integer between 1 an 5
    while True:
        try:
            pl_cnt = int(input("How many players? (Up to 5) "))
            if 0 < pl_cnt <= 5:
                break
        except KeyboardInterrupt:
            exitBowling()
        except:
            pass
        #In case of wrong input:
        moveUpAndClean()
    return pl_cnt


def getPlayers(pl_cnt):
    #Get players names
    #Any values allowed except empty strings and strings of blanks
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
            #In case of wrong input:
            moveUpAndClean()
        #Add new player
        p.append(Player(p_name))
    return p


def setScreen(players):
    #Draw initial screen with empty displays

    #Clear screen and leave 3 lines for input prompts.
    clearScreen()
    moveByLine('B', 3)

    #Draw empty display for each player
    for i, player in enumerate(players):
        #Move one line down from previous section
        moveByLine('B', 1)
        #Print player's name
        print('Player #' + str(i + 1) + ': ' + player.name)
        #Print cells for throws
        print('|__' * 21 + '|')
        #Print cells for results
        print('|_____' * 9 + '|________|')


def showUpperScore(score, throw, turn, order):
    #Show player's score after a throw is upper cells
    #score - result of a throw
    #throw - throw number (1, 2 or 3)
    #turn - turn number (1..10)
    #order - player number (1..players_count)

    #Add extra __ for format
    score = '__' + str(score)
    #Move to current position inside a display
    moveXY(6 + 4*(order - 1), 2 + 6*turn + 3*(throw - 1))
    #Print last 2 chars from the score. 
    print(score[-2:], end='')


def showLowerScore(player, order):
    #Show player's results in bottom cells
    #player - player object
    #order - player number (1..players_count)

    score = ''
    #Compose bottom display for exixting results
    for i, p in enumerate(player.points):
        score += '|__' 
        if i == 9:
            #Add extra _ for final cell
            score += '_'
        score += str(p[3]) + '_'
        if len(str(p[3])) == 1:
            #Add expta _ for one digit score
            score += '_'
    #Print results from the beginnig of player's display
    moveXY(7 + 4*(order - 1), 1)
    print(score, end='')


def showTotalScore(player, order):
    total = 0
    for p in player.points:
        total += p[3]
    
    total = str(total)

    print('\033[32m', end='')
    moveXY(6 + 4*(order), 65)
    print('Total', end='')
    print('\033[0m', end='')
    print('|', end='')

    moveXY(7 + 4*(order), 65)
    print("_" * (4 - len(total)), end='')
    print('\033[32m', end='')
    print(total[-5:], end='')
    print('\033[0m', end='')
    print('_|', end='')


def getThrow(msg, last_throw, is_last):
    #Show a message for current player and get result of a throw
    #msg - prompt message
    #last_throw - last score for current player
    #is_last - True if it is the last round

    moveHome()
    cleanLine()
    
    while True:
        try:
            score = int(input(msg))
            #Different check for the last round: it is possible to get two 10s in a row
            if ((0 <= score + last_throw <= 10) and not is_last) or ((0 <= score <= 10) and is_last):
                break
        except KeyboardInterrupt:
            exitBowling()
        except:
            pass
        #In case of wrong input:
        moveUpAndClean()

    return score


#Main part
#Clear screen & move to the top
clearScreen()

#Get number of players
players_count = getNumberOfPlayers()
#Get players
players = getPlayers(players_count)
#Set initial screen
setScreen(players)

#Start 10 rounds
for i in range(10):
    #Enumerate players
    for p, player in enumerate(players):
        #Compose message for throw prompt
        score_msg = 'Round #' + str(i + 1) + ': ' + player.name
        #Get first throw
        first_trow = getThrow(score_msg + ", what is your 1st score? ", 0, False)

        #Show score after the first throw
        showUpperScore(first_trow, 1, i, p + 1)

        #Check strike for 2 previous results
        if i > 0:
            if player.points[-1][3] == 'X':
                if i > 1:
                    if player.points[-2][3] == 'X' and len(player.points) > 1:
                        #If there were 2 consecutive strikes, fill first strike
                        player.points[-2][3] = 20 + first_trow

        #Check spare in previous result
        if i > 0:
            if player.points[-1][3] == '/' and player.points:
                #Fill previous result if it was strike
                player.points[-1][3] = 10 + first_trow

        #Show updated results
        showLowerScore(player, p + 1)

        #Check if it was a strike
        if first_trow == 10 and i < 9:
            #Set current result as strike
            player.points.append([first_trow, 0, '', "X"])

            #Show updated results
            showLowerScore(player, p + 1)
        else:
            #Check if it the last round
            if i == 9:
                is_last = True
            else:
                is_last = False

            #Get second throw
            second_throw = getThrow(score_msg + ", what is your 2nd score? ", first_trow, is_last)

            #Show score after the second throw
            showUpperScore(second_throw, 2, i, p + 1)

            #Check if previous result was a strike
            if i > 0:
                if player.points[-1][3] == 'X' and player.points:
                    #Update previous result
                    player.points[-1][3] = 10 + first_trow + second_throw
            
            #Show updated results
            showLowerScore(player, p + 1)
            
            if not is_last:
                #If is not the last round, check for a spare
                if first_trow + second_throw == 10:
                    #Set current result as spare
                    player.points.append([first_trow, second_throw, '', "/"])
                    
                    #Show updated results
                    showLowerScore(player, p + 1)
                else:
                    #Set regular result
                    player.points.append([first_trow, second_throw, '', first_trow + second_throw])

                    #Show updated results
                    showLowerScore(player, p + 1)
            else:
                #if is the last round, check if player may perform third throw
                if first_trow == 10 or (first_trow + second_throw == 10):

                    #Get third throw
                    tird_throw = getThrow(score_msg + ", what is your 3rd score? ", second_throw, True)
                    
                    #Show score after the third throw
                    showUpperScore(tird_throw, 3, i, p + 1)
                    
                    #Set results for all three throws
                    player.points.append([first_trow, second_throw, tird_throw, first_trow + second_throw + tird_throw])
                else:
                    #Set regular result
                    player.points.append([first_trow, second_throw, '', first_trow + second_throw])

                #Show updated results
                showLowerScore(player, p + 1)

#Show total scores
for p, player in enumerate(players):
    showTotalScore(player, p)

#Move 3 lines down before exit
moveByLine('B', 3)