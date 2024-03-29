# -----------------------------------------------------------------------------
# Name:        Match and Snatch
# Purpose:     A description of your program goes here.
#
# Author:      Michal Buczek
# Created:     06-May-2022
# Updated:     01-June-2022
# -----------------------------------------------------------------------------
# I think this project deserves a level 4+ because I have all the necessary features from levels 1-4 such as;
# (user-friendly interface, loops, lists, dictionary, read and write file, proper naming conventions, game states, etc.)
# I have also challenged myself by incorporating other concepts we may have learnt in class or even outside of class
# with a little self learning. These cool new concepts are listed in the Features Added section below.
# Overall I enjoyed the process of making this game, and
# I worked really hard to make daily commits.
#
# Features Added:
#   1. Flip animation: Probably the hardest feature to add. I ran into lots of bugs and fixed them with dictionary use
#   and nat saving all variables
#   2. Player name input: Making the letters pop up on the screen visually in real time was a challenge, but I managed
#   to get it done by implementing a similar strategy from a source that I referenced.
#   3. Making a text paragraph: Using another source I was able to make a function which makes lines under previous text
#   when reaching the right side of the screen.
#   4. Two game modes: Pvp and solo which have separate objectives. PVP objective to get most pairs, solo objective to
#   beat the high score which is saved in a readable file.
#   5. Time reading which makes cards flip back down after 2 seconds following the click.
# -----------------------------------------------------------------------------
import pygame
import random
import time
from pygame.locals import *

# -----------------------------Setup------------------------------------------------------#
pygame.init()  # Prepare the pygame module for use
surfaceSize = 900  # Desired physical surface size, in pixels.

clock = pygame.time.Clock()  # Force frame rate to be slower

# Create surface of (width, height), and its window.
mainSurface = pygame.display.set_mode((surfaceSize - 100, surfaceSize))


#  Makes text lines that go under previous one when reached width of the screen
#  Function found on https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
def blit_text(surface, text, pos, font, color=pygame.Color('white')):
    sentences = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space is the width of one letter.
    maxWidth = surfaceSize - 100
    x, y = pos
    for line in sentences:
        for word in line:
            wordSurface = font.render(word, 0, color)
            wordWidth, wordHeight = wordSurface.get_size()
            if x + wordWidth >= maxWidth:
                x = pos[0]  # Reset the x.
                y += wordHeight  # Start on new row.
            surface.blit(wordSurface, (x, y))
            x += wordWidth + space
        x = pos[0]  # Reset the x.


def main():
    # -----------------------------Program Variable Initialization----------------------------#

    #  game state
    gameState = "menu"

    #  Menu screen game state variables -----------------------------------------------------

    # Background
    lobbyBackground = pygame.image.load('menuScreenBG.jpg')
    lobbyBackground = pygame.transform.smoothscale(lobbyBackground, (surfaceSize - 100, surfaceSize))

    #  Title font
    gameName = pygame.font.SysFont('impact', 85)

    #  Play button position
    playButPos = (275, 400, 250, 100)
    #  play text
    playTxt = pygame.font.SysFont('lucidaconsole', 70)

    #  How to play button position
    howToButPos = (275, 530, 250, 50)
    #  How to play text
    howToPlayTxt = pygame.font.SysFont('lucidaconsole', 35)

    #  Game mode selection buttons positions
    soloButPos = [560, 400, 100, 35]
    gameModeFont = pygame.font.SysFont('lucidaconsole', 25)
    soloColour = (255, 255, 255)
    pvpButPos = [560, 450, 100, 35]
    pvpColour = (255, 255, 255)
    soloFill = False
    pvpFill = False

    #  User game names (pvp) Manually typed
    p1NamePick = True
    p2NamePick = False
    names = False
    p1NameBox = [275, 600, 250, 30]
    p2NameBox = [275, 650, 250, 30]
    player1Name = ""
    player2Name = ""
    name1 = gameModeFont.render(player1Name, True, (255, 0, 0))
    textBox1 = name1.get_rect()
    textBox1.topleft = (330, 604)
    cursor1 = pygame.Rect(textBox1.topright, (3, textBox1.height))
    p1NameTooLong = False
    p2NameTooLong = False
    name2 = gameModeFont.render(player2Name, True, (0, 0, 255))
    textBox2 = name2.get_rect()
    textBox2.topleft = (330, 654)
    cursor2 = pygame.Rect(textBox2.topright, (3, textBox2.height))
    #  Variables that represent whether they inputted a name or not
    name1Inputted = False
    name2Inputted = False
    asterix1 = False
    asterix2 = False

    #  Check mark
    check = pygame.image.load('check.png')
    check = pygame.transform.scale(check, (80, 80))

    #  How to play screen variables --------------------------------------------------------
    #  Background
    htpBackground = pygame.image.load('htpScreenBG.jpg')
    htpBackground = pygame.transform.smoothscale(htpBackground, (surfaceSize + 100, surfaceSize + 60))
    #  instructions text
    rules = "Ready to put your memory to the test and have a great time? Well then your in the right place! " \
            "To play match and snatch, simply click on two cards to reveal and see if theres a match. " \
            "If playing solo, try to get all the matches with the least amount of card clicks. " \
            "If playing head to head, try to collect the most pairs"
    instructionFont = pygame.font.SysFont('arial', 30)
    #  return button pos
    returnPos = (325, 550, 150, 50)
    returnFont = pygame.font.SysFont('impact', 40)

    #  main game state variables ------------------------------------------------------------

    gameMode = "solo"

    cardsBackground = pygame.image.load('cardGameBg.jpg')  # game background
    cardsBackground = pygame.transform.scale(cardsBackground, (surfaceSize, surfaceSize))
    #  Card variables
    cardsBack = pygame.image.load("card_back.png")
    cardsFront = pygame.image.load("card_front.png")
    cardsPos = [(50, 100), (200, 100), (350, 100), (500, 100), (650, 100), (50, 300), (200, 300), (350, 300),
                (500, 300),
                (650, 300), (50, 500), (200, 500), (350, 500), (500, 500), (650, 500), (50, 700), (200, 700),
                (350, 700), (500, 700), (650, 700)]

    numberOfCards = 20
    #  Makes all the cards back visible and all card fronts invisible
    visible = [True for _ in range(numberOfCards)]
    sideUp = [False for _ in range(numberOfCards)]
    selectedCard2 = -1
    selectedCard = -1

    # card flipping animation
    animation = {}
    animationTwo = {}

    oneCardUp = False  # When no cards are flipped up this is false
    upTime = 0  # Time that both cards are flipped up, starting at 0
    secondCardUp = False  # Second card flip recognition (False when no second card flipped, True when two cards up)
    #  Sprites
    demon = pygame.image.load('big_demon_idle_anim_f0.png')
    doubledDemon = pygame.transform.scale2x(demon)
    zombie = pygame.image.load('big_zombie_idle_anim_f0.png')
    doubledZombie = pygame.transform.scale2x(zombie)
    elf = pygame.image.load('elf_m_hit_anim_f0.png')
    doubledElf = pygame.transform.scale2x(elf)
    flask = pygame.image.load('flask_big_blue.png')
    doubledFlask = pygame.transform.scale2x(flask)
    goblin = pygame.image.load('goblin_idle_anim_f0.png')
    doubledGoblin = pygame.transform.scale2x(goblin)
    iceZombie = pygame.image.load('ice_zombie_run_anim_f0.png')
    doubledIceZombie = pygame.transform.scale2x(iceZombie)
    knight = pygame.image.load('knight_f_hit_anim_f0.png')
    doubledKnight = pygame.transform.scale2x(knight)
    lizard = pygame.image.load('lizard_m_idle_anim_f1.png')
    doubledLizard = pygame.transform.scale2x(lizard)
    swampy = pygame.image.load('swampy_idle_anim_f1.png')
    doubledSwampy = pygame.transform.scale2x(swampy)
    wizzard = pygame.image.load('wizzard_m_idle_anim_f1.png')
    doubledWizzard = pygame.transform.scale2x(wizzard)

    #  Random sprite card order
    sprites = [(doubledDemon, 1), (doubledDemon, 1), (doubledZombie, 2), (doubledZombie, 2), (doubledElf, 3),
               (doubledElf, 3), (doubledFlask, 4), (doubledFlask, 4), (doubledGoblin, 5), (doubledGoblin, 5),
               (doubledIceZombie, 6), (doubledIceZombie, 6), (doubledKnight, 7), (doubledKnight, 7), (doubledLizard, 8),
               (doubledLizard, 8), (doubledSwampy, 9), (doubledSwampy, 9), (doubledWizzard, 10), (doubledWizzard, 10)]
    random.shuffle(sprites)  # shuffles the order when the game is run

    #  cards selected, if both are the same Sprite then it is a match
    card1 = -1
    card2 = -2

    #  Click counter font
    counter = pygame.font.SysFont('impact', 45)
    clickCount = 0  # amount of card clicks counter set to 0
    highScore = open('highScore', 'r')
    lowestNumber = highScore.readlines()
    highScore.close()
    lowestNumber = int(lowestNumber[0])

    #  Player vs Player score counter
    player1Score = 0
    player2Score = 0
    matchCountFont = pygame.font.SysFont('impact', 40)
    p1Turn = True
    p2Turn = False

    #  Game Over State variables --------------------------------------------------------------

    gameOverBG = pygame.image.load('endScreenBG.jpg')
    gameOverBG = pygame.transform.scale(gameOverBG, (surfaceSize + 200, surfaceSize))

    #  Game over font
    headline = pygame.font.SysFont('impact', 120)

    #  The number of pairs that have been found and have disappeared
    noPair = 0

    #  Play again button
    replayButPos = [250, 500, 300, 100]
    playAgain = pygame.font.SysFont('lucidaconsole', 40)

    #  return to lobby button position
    returnLobPos = [250, 625, 300, 100]

    #  Lowest score text
    lowestClicks = pygame.font.SysFont('lucidaconsole', 25)

    winnerFont = pygame.font.SysFont('lucidaconsole', 25)

    # -----------------------------Main Program Loop---------------------------------------------#
    while True:
        # -----------------------------Event Handling-----------------------------------------#

        ev = pygame.event.poll()  # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break  # ... leave game loop

        #  Starting screen
        if gameState == "menu":
            #  Event Handling ------------------------------------------------------------------
            #  play button click detection
            mousePos = pygame.mouse.get_pos()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if playButPos[0] <= mousePos[0] <= playButPos[0] + 250 and \
                        playButPos[1] <= mousePos[1] <= playButPos[1] + 100:
                    if gameMode == "pvp" and name1Inputted and name2Inputted or gameMode == "solo":
                        gameState = "main game"
                        visible = [True for _ in range(numberOfCards)]
                        sideUp = [False for _ in range(numberOfCards)]
                        noPair = 0
                        clickCount = 0
                        random.shuffle(sprites)
                        player1Score = 0
                        player2Score = 0
                    elif not name1Inputted and not name2Inputted:
                        #  doubleAsterix = True
                        asterix1 = True
                        asterix2 = True
                    elif not name1Inputted:
                        asterix1 = True
                    elif not name2Inputted:
                        asterix2 = True

                    #  Make sure to make a function that resets variables incase they go from end screen to menu
                #  how to play button click recognition
                elif howToButPos[0] <= mousePos[0] <= howToButPos[0] + 250 and \
                        howToButPos[1] <= mousePos[1] <= howToButPos[1] + 50:
                    gameState = "how to play"
                #  Game mode selection click recognition
                elif soloButPos[0] <= mousePos[0] <= soloButPos[0] + 100 and \
                        soloButPos[1] <= mousePos[1] <= soloButPos[1] + 35:
                    gameMode = "solo"
                    soloFill = True
                    pvpFill = False
                elif pvpButPos[0] <= mousePos[0] <= pvpButPos[0] + 100 and \
                        pvpButPos[1] <= mousePos[1] <= pvpButPos[1] + 35:
                    gameMode = "pvp"
                    pvpFill = True
                    soloFill = False

            if names:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if p1NameBox[0] <= mousePos[0] <= p1NameBox[0] + 250 and \
                            p1NameBox[1] <= mousePos[1] <= p1NameBox[1] + 30:
                        p1NamePick = True
                        p2NamePick = False
                    elif p2NameBox[0] <= mousePos[0] <= p2NameBox[0] + 250 and \
                            p2NameBox[1] <= mousePos[1] <= p2NameBox[1] + 30:
                        p2NamePick = True
                        p1NamePick = False
                #  Makes the text update in real time and display on the screen, reference used:
                #  https://pygame.readthedocs.io/en/latest/4_text/text.html#edit-text-with-the-keybord
                if ev.type == KEYDOWN:
                    if ev.key == K_BACKSPACE:
                        if p1NamePick:  # Player inputs their game name
                            if len(player1Name) > 0:
                                name1 = gameModeFont.render(player1Name, True, (255, 0, 0))
                                textBox1.size = name1.get_size()
                                player1Name = player1Name[:-1]
                                cursor1.topleft = textBox1.topright
                                if textBox1[2] + 70 < p1NameBox[2]:
                                    p1NameTooLong = False
                        elif p2NamePick:
                            if len(player2Name) > 0:
                                name2 = gameModeFont.render(player2Name, True, (255, 0, 0))
                                textBox2.size = name2.get_size()
                                player2Name = player2Name[:-1]
                                cursor2.topleft = textBox2.topright
                                if textBox2[2] + 70 < p2NameBox[2]:
                                    p2NameTooLong = False
                    else:
                        if p1NamePick:  # Makes sure that the name is not too long
                            if not p1NameTooLong:
                                player1Name += ev.unicode
                                name1 = gameModeFont.render(player1Name, True, (255, 0, 0))
                                textBox1.size = name1.get_size()
                                cursor1.topleft = textBox1.topright
                                cursor1[0] += 15  # Makes the cursor on the end of the letters
                                if textBox1[2] + 70 >= p1NameBox[2]:
                                    p1NameTooLong = True
                        elif p2NamePick:
                            if not p2NameTooLong:
                                player2Name += ev.unicode
                                name2 = gameModeFont.render(player2Name, True, (0, 200, 255))
                                textBox2.size = name2.get_size()
                                cursor2.topleft = textBox2.topright
                                cursor2[0] += 15
                                if textBox2[2] + 70 >= p2NameBox[2]:
                                    p2NameTooLong = True
                            mainSurface.blit(name1, textBox1)
                            mainSurface.blit(name2, textBox2)
            #  logic ---------------------------------------------------------------------
            if gameMode == "pvp":
                names = True
                pvpFill = True
            elif gameMode == "solo":
                names = False
                soloFill = True

            #  Drawing Everything --------------------------------------------------------------

            #  Background image
            mainSurface.blit(lobbyBackground, (0, 0))

            #  Title
            gameTitle = gameName.render("Match & Snatch", False, (255, 255, 255))
            mainSurface.blit(gameTitle, (185, 150))

            #  Play button
            pygame.draw.rect(mainSurface, (242, 200, 75), playButPos, 5)
            #  Play text
            playGame = playTxt.render("PLAY", False, (255, 255, 255))
            mainSurface.blit(playGame, (playButPos[0] + 40, playButPos[1] + 15))

            #  How to play button
            pygame.draw.rect(mainSurface, (255, 255, 255), howToButPos, 3)
            helpTxt = howToPlayTxt.render("How to Play", False, (242, 200, 75))
            mainSurface.blit(helpTxt, (howToButPos[0] + 10, howToButPos[1] + 5))

            #  Game mode selection buttons
            #  Fills back colour of selected game mode
            if soloFill:
                pygame.draw.rect(mainSurface, (0, 255, 255), soloButPos)
                soloColour = (0, 0, 0)
                pvpColour = (255, 255, 255)
            elif pvpFill:
                pygame.draw.rect(mainSurface, (0, 255, 255), pvpButPos)
                pvpColour = (0, 0, 0)
                soloColour = (255, 255, 255)

            #  Game mode buttons
            pygame.draw.rect(mainSurface, (255, 255, 255), soloButPos, 3)
            soloText = gameModeFont.render("Solo", False, soloColour)
            mainSurface.blit(soloText, (soloButPos[0] + 20, soloButPos[1] + 5))
            pygame.draw.rect(mainSurface, (255, 255, 255), pvpButPos, 3)
            pvpText = gameModeFont.render("PVP", False, pvpColour)
            mainSurface.blit(pvpText, (pvpButPos[0] + 30, pvpButPos[1] + 5))

            #  Name boxes for pvp
            if names:
                pygame.draw.rect(mainSurface, (255, 0, 0), p1NameBox, 2)
                pygame.draw.rect(mainSurface, (0, 200, 255), p2NameBox, 2)
                p1NameSlot = gameModeFont.render(f"P1: {player1Name}", False, (255, 0, 0))
                mainSurface.blit(p1NameSlot, (p1NameBox[0] + 10, p1NameBox[1] + 4))
                p2NameSlot = gameModeFont.render(f"P2: {player2Name}", False, (0, 200, 255))
                mainSurface.blit(p2NameSlot, (p2NameBox[0] + 10, p2NameBox[1] + 4))
                #  Check marks
                if len(player1Name) > 0:
                    mainSurface.blit(check, (530, 590))
                    name1Inputted = True
                    asterix1 = False
                elif len(player1Name) == 0:
                    name1Inputted = False
                    asterix2 = False

                if len(player2Name) > 0:
                    mainSurface.blit(check, (530, 640))
                    name2Inputted = True
                elif len(player2Name) == 0:
                    name2Inputted = False

                #  type username text
                if not name1Inputted:
                    typeUsername1 = gameModeFont.render("Type Username", True, (255, 255, 255))
                else:
                    typeUsername1 = gameModeFont.render("", False, (255, 255, 255))
                mainSurface.blit(typeUsername1, (330, 604))

                if not name2Inputted:
                    typeUsername2 = gameModeFont.render("Type Username", True, (255, 255, 255))
                else:
                    typeUsername2 = gameModeFont.render("", False, (255, 255, 255))
                mainSurface.blit(typeUsername2, (330, 654))

                #  Makes the cursor pop up and disappear every second
                if p1NamePick:
                    if time.time() % 1 > 0.5:
                        pygame.draw.rect(mainSurface, (255, 0, 0), cursor1)
                elif p2NamePick:
                    if time.time() % 1 > 0.5:
                        pygame.draw.rect(mainSurface, (0, 200, 255), cursor2)

                #  Draws asterisk's if pvp and names aren't typed in
                if asterix1 and asterix2:
                    asterix = gameModeFont.render("*", False, (255, 255, 255))
                    mainSurface.blit(asterix, (250, 604))
                    mainSurface.blit(asterix, (250, 654))
                elif asterix1:
                    asterix = gameModeFont.render("*", False, (255, 255, 255))
                    mainSurface.blit(asterix, (250, 604))
                elif asterix2:
                    asterix = gameModeFont.render("*", False, (255, 255, 255))
                    mainSurface.blit(asterix, (250, 654))

        #  How to play game state
        elif gameState == "how to play":
            #  Events -------------------------------------------------------
            mousePos = pygame.mouse.get_pos()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if returnPos[0] <= mousePos[0] <= returnPos[0] + 150 and \
                        returnPos[1] <= mousePos[1] <= returnPos[1] + 50:
                    gameState = "menu"

            #  Drawing everything --------------------------------------------
            mainSurface.blit(htpBackground, (-100, 0))  # Background
            #  Title
            howToPlay = headline.render("Instructions", False, (255, 255, 255))
            mainSurface.blit(howToPlay, (160, 180))
            #  instructions
            blit_text(mainSurface, rules, (20, 320), instructionFont)
            # return button
            pygame.draw.rect(mainSurface, (242, 200, 75), returnPos, 3)
            backHome = returnFont.render("Return", False, (255, 255, 255))
            mainSurface.blit(backHome, (355, 563))

        #  in game state
        elif gameState == "main game":

            #  Event Handling -------------------------------------------------------------------

            #  Makes the mouse click faster and run smoother because it doesn't consider the mouses motion or when
            #  there is no event
            if ev.type == pygame.MOUSEMOTION:
                continue
            #  Mouse position and click recognition
            if oneCardUp:  # Allows second card to be flipped
                if ev.type == pygame.MOUSEBUTTONDOWN and not secondCardUp:
                    mouseX, mouseY = ev.pos
                    for i in range(numberOfCards):
                        if i != selectedCard and \
                                cardsPos[i][0] <= mouseX <= cardsPos[i][0] + 100 and \
                                cardsPos[i][1] <= mouseY <= cardsPos[i][1] + 180:
                            animation[i] = 1
                            selectedCard2 = i
                            upTime = pygame.time.get_ticks()
                            secondCardUp = True
                            sideUp[i] = True
                            card2 = sprites[i][1]
                            clickCount += 1
                            break

            else:  # When no card is face up this is possible
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = ev.pos
                    for i in range(numberOfCards):
                        if cardsPos[i][0] <= mouseX <= cardsPos[i][0] + 100 and \
                                cardsPos[i][1] <= mouseY <= cardsPos[i][1] + 180:
                            animation[i] = 1
                            oneCardUp = True
                            selectedCard = i
                            sideUp[i] = True
                            card1 = sprites[i][1]
                            clickCount += 1
                            break

            # -----------------------------Program Logic---------------------------------------------#
            #  Gets the current time of the program run time
            currentTime = pygame.time.get_ticks()

            #  Checks if the card sprites that are flipped up are a match
            if card1 == card2:
                if upTime > 0 and currentTime - upTime > 2000:
                    #  Makes the cards disappear
                    visible[selectedCard] = False
                    visible[selectedCard2] = False
                    sideUp[selectedCard] = False
                    sideUp[selectedCard2] = False
                    noPair += 1  # Increases by one every time a pair disappears
                    if gameMode == "pvp":
                        if p1Turn:
                            player1Score += 1
                            p1Turn = False
                            p2Turn = True
                        elif p2Turn:
                            player2Score += 1
                            p2Turn = False
                            p1Turn = True

            #  When both cards are flipped up, this makes sure that they go back down automatically after one second
            if upTime > 0 and currentTime - upTime > 2000:
                sideUp[selectedCard] = False
                sideUp[selectedCard2] = False
                animation = {selectedCard: 1, selectedCard2: 1}
                animationTwo = {}
                selectedCard = -1
                selectedCard2 = -1
                oneCardUp = False
                secondCardUp = False
                card1 = -1
                card2 = -2
                upTime = 0
                if gameMode == "pvp":
                    if p1Turn:
                        p1Turn = False
                        p2Turn = True
                    elif p2Turn:
                        p2Turn = False
                        p1Turn = True

            #  Checks if all card matches are gone and if so changes to game over state
            if noPair >= 10:
                gameState = "game over"
                #  Saves highscores to a file for future use
                if gameMode == "solo" and clickCount < int(lowestNumber):
                    highScore = str(clickCount)
                    highScoreFile = open('highScore', 'w')
                    highScoreFile.write(highScore)
                    highScoreFile.close()

            # -----------------------------Drawing Everything-------------------------------------#
            mainSurface.blit(cardsBackground, (0, 0))

            #  Drawing cards
            #  Back of card
            for i in range(numberOfCards):
                if visible[i]:  # Checks if the card is being drawn
                    if sideUp[i]:  # Front of card
                        if i in animation:
                            scale = animation[i]
                            scale -= 0.05  # scales down the image width
                            animation[i] = scale
                            if scale > 0:  # checks if the card back is still visible
                                widthBack = scale * cardsBack.get_width()  # decreases the width of the card by scale
                                heightBack = cardsBack.get_height()
                                card = pygame.transform.scale(cardsBack, (widthBack, heightBack))
                                mainSurface.blit(card, cardsPos[i])
                            else:  # if the card back is invisible (<=0) then it gets rid of the animation index
                                animation.pop(i)
                                animationTwo[i] = 0
                        elif i in animationTwo:  # When the second animation is present in the dictionary
                            scale = animationTwo[i]
                            scale += 0.05
                            animationTwo[i] = scale
                            if scale < 1:  # continues if the card is smaller than its regular size
                                widthFront = scale * cardsFront.get_width()
                                heightFront = cardsFront.get_height()
                                card = pygame.transform.scale(cardsFront, (widthFront, heightFront))
                                mainSurface.blit(card, cardsPos[i])
                                sprite = sprites[i][0]  # Makes the sprite go through the same motion as the card front
                                widthSprite = scale * sprite.get_width()
                                heightSprite = sprite.get_height()
                                image = pygame.transform.scale(sprite, (widthSprite, heightSprite))
                                mainSurface.blit(image, (cardsPos[i][0] + 20 * scale, cardsPos[i][1] + 30))
                            else:
                                animationTwo.pop(i)  # When the card front is regular size it pops the index and value
                        else:
                            mainSurface.blit(cardsFront, cardsPos[i])
                            mainSurface.blit(sprites[i][0], (cardsPos[i][0] + 20, cardsPos[i][1] + 30))
                    else:  # The opposite operation where the flip is from front back to down
                        if i in animation:
                            scale = animation[i]
                            scale -= 0.05
                            animation[i] = scale
                            if scale > 0:
                                width = scale * cardsFront.get_width()
                                height = cardsFront.get_height()
                                card = pygame.transform.scale(cardsFront, (width, height))
                                mainSurface.blit(card, cardsPos[i])

                                sprite = sprites[i][0]
                                widthSprite = scale * sprite.get_width()
                                heightSprite = sprite.get_height()
                                image = pygame.transform.scale(sprite, (widthSprite, heightSprite))
                                mainSurface.blit(image, (cardsPos[i][0] + 20 * scale, cardsPos[i][1] + 30))
                            else:
                                animation.pop(i)
                                animationTwo[i] = 0

                        elif i in animationTwo:
                            scale = animationTwo[i]
                            scale += 0.05
                            animationTwo[i] = scale
                            if scale < 1:
                                widthBack = scale * cardsBack.get_width()
                                heightBack = cardsBack.get_height()
                                card = pygame.transform.scale(cardsBack, (widthBack, heightBack))
                                mainSurface.blit(card, cardsPos[i])
                            else:
                                animationTwo.pop(i)
                        else:
                            mainSurface.blit(cardsBack, cardsPos[i])

            #  Click counter
            if gameMode == "solo":
                clickCounter = counter.render(f"Clicks: {clickCount}", False, (255, 255, 255))
                mainSurface.blit(clickCounter, (10, 10))

            #  Player vs Player score counter
            elif gameMode == "pvp":
                p1Count = matchCountFont.render(f"{player1Name}: {player1Score}", False, (255, 0, 0))
                mainSurface.blit(p1Count, (10, 10))
                p2Count = matchCountFont.render(f"{player2Name}: {player2Score}", False, (0, 200, 255))
                mainSurface.blit(p2Count, (10, 50))
                if p1Turn:
                    p1TurnIndicator = matchCountFont.render(f"{player1Name}'s Turn", False, (255, 0, 0))
                    mainSurface.blit(p1TurnIndicator, (520, 10))
                elif p2Turn:
                    p2TurnIndicator = matchCountFont.render(f"{player2Name}'s Turn", False, (0, 200, 255))
                    mainSurface.blit(p2TurnIndicator, (520, 50))

        #  End game state
        elif gameState == "game over":
            mousePos = pygame.mouse.get_pos()
            #  Event handling --------------------------------------------------------------
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if replayButPos[0] <= mousePos[0] <= replayButPos[0] + 300 and \
                        replayButPos[1] <= mousePos[1] <= replayButPos[1] + 100:
                    gameState = "main game"
                    visible = [True for _ in range(numberOfCards)]
                    sideUp = [False for _ in range(numberOfCards)]
                    noPair = 0
                    clickCount = 0
                    random.shuffle(sprites)
                    player1Score = 0
                    player2Score = 0
                    animation = {}
                    animationTwo = {}
                elif returnLobPos[0] <= mousePos[0] <= returnLobPos[0] + 300 and \
                        returnLobPos[1] <= mousePos[1] <= returnLobPos[1] + 100:
                    gameState = "menu"

            #  Drawing everything -----------------------------------------------------------
            mainSurface.blit(gameOverBG, (0, 0))

            #  End game text
            endGame = headline.render("Game Over", False, (255, 255, 255))
            mainSurface.blit(endGame, (175, 150))

            #  Final click count
            score = counter.render(f"Total Clicks: {clickCount}", False, (255, 255, 255))
            mainSurface.blit(score, (300, 260))

            #  play again button
            pygame.draw.rect(mainSurface, (255, 255, 255), replayButPos, 5)
            replayText = playAgain.render('Play Again', False, (0, 255, 0))
            mainSurface.blit(replayText, (replayButPos[0] + 30, replayButPos[1] + 30))

            #  return to lobby button
            pygame.draw.rect(mainSurface, (0, 255, 0), returnLobPos, 5)
            lobbyText = playAgain.render('Lobby', False, (255, 255, 255))
            mainSurface.blit(lobbyText, (returnLobPos[0] + 90, returnLobPos[1] + 30))

            #  Lowest click score display
            if gameMode == "solo":
                readHighScore = open('highScore', 'r')
                fileRead = readHighScore.readlines()
                readHighScore.close()
                lowHighScore = lowestClicks.render(f'HighScore: {fileRead[0]}', False, (0, 255, 0))
                mainSurface.blit(lowHighScore, (310, 320))

            elif gameMode == "pvp":
                if player1Score > player2Score:
                    p1Wins = winnerFont.render(f'{player1Name} wins with {player1Score} matches', False, (0, 255, 0))
                    mainSurface.blit(p1Wins, (230, 320))
                elif player2Score > player1Score:
                    p2Wins = winnerFont.render(f'{player2Name} wins with {player2Score} matches', False, (0, 255, 0))
                    mainSurface.blit(p2Wins, (230, 320))
                else:
                    tie = winnerFont.render(f'Its a tie between {player1Name} and {player2Name}', False, (0, 255, 0))
                    mainSurface.blit(tie, (160, 320))

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60)  # Force frame rate to be slower

    pygame.quit()  # Once we leave the loop, close the window.


main()
