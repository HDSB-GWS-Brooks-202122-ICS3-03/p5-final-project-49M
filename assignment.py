# -----------------------------------------------------------------------------
# Name:        Match and Snatch
# Purpose:     A description of your program goes here.
#
# Author:      Michal Buczek
# Created:     06-May-2022
# Updated:     13-Sept-2020
# -----------------------------------------------------------------------------
# I think this project deserves a level XXXXXX because ...
#
# Features Added:
#   ...
#   ...
#   ...
# -----------------------------------------------------------------------------
import pygame
import random

# -----------------------------Setup------------------------------------------------------#
pygame.init()  # Prepare the pygame module for use
surfaceSize = 900  # Desired physical surface size, in pixels.

clock = pygame.time.Clock()  # Force frame rate to be slower

# Create surface of (width, height), and its window.
mainSurface = pygame.display.set_mode((surfaceSize - 100, surfaceSize))


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
                    gameState = "main game"
                    #  Make sure to make a function that resets variables incase they go from end screen to menu
                #  how to play button click recognition
                elif howToButPos[0] <= mousePos[0] <= howToButPos[0] + 250 and \
                        howToButPos[1] <= mousePos[1] <= howToButPos[1] + 50:
                    gameState = "how to play"
            #  logic ---------------------------------------------------------------------
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
                        if i != selectedCard and cardsPos[i][0] <= mouseX <= cardsPos[i][0] + 100 and \
                                cardsPos[i][1] <= mouseY <= cardsPos[i][1] + 180:
                            selectedCard2 = i
                            upTime = pygame.time.get_ticks()
                            secondCardUp = True
                            sideUp[i] = True
                            card2 = sprites[i][1]
                            clickCount += 1
                            break

            elif not oneCardUp:  # When no card is face up this is possible
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = ev.pos
                    for i in range(numberOfCards):
                        if cardsPos[i][0] <= mouseX <= cardsPos[i][0] + 100 and \
                                cardsPos[i][1] <= mouseY <= cardsPos[i][1] + 180:
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
                if upTime > 0 and currentTime - upTime > 1000:
                    print("match")
                    #  Makes the cards disappear
                    visible[selectedCard] = False
                    visible[selectedCard2] = False
                    sideUp[selectedCard] = False
                    sideUp[selectedCard2] = False
                    noPair += 1  # Increases by one every time a pair disappears

            #  When both cards are flipped up, this makes sure that they go back down automatically after one second
            if upTime > 0 and currentTime - upTime > 1000:
                sideUp[selectedCard] = False
                sideUp[selectedCard2] = False
                selectedCard2 = False
                oneCardUp = False
                upTime = 0
                secondCardUp = False
                card1 = -1
                card2 = -2

                #  Checks if all card matches are gone and if so changes to game over state
                if noPair >= 10:
                    gameState = "game over"

            # -----------------------------Drawing Everything-------------------------------------#
            mainSurface.blit(cardsBackground, (0, 0))

            #  Drawing cards
            #  Back of card
            for i in range(numberOfCards):
                if visible[i]:
                    cardImage = cardsBack
                    mainSurface.blit(cardImage, cardsPos[i])
                    if sideUp[i]:  # Front of card
                        cardImage = cardsFront
                        mainSurface.blit(cardImage, cardsPos[i])
                        mainSurface.blit(sprites[i][0], (cardsPos[i][0] + 20, cardsPos[i][1] + 30))

            #  Click counter
            clickCounter = counter.render(f"Clicks: {clickCount}", False, (255, 255, 255))
            mainSurface.blit(clickCounter, (10, 10))

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

            #  Program Logic ----------------------------------------------------------------
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

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60)  # Force frame rate to be slower

    pygame.quit()  # Once we leave the loop, close the window.


main()
