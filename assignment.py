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
import time


def timeNow():
    return int(time.time())


def main():
    # -----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()  # Prepare the pygame module for use
    surfaceSize = 900  # Desired physical surface size, in pixels.

    clock = pygame.time.Clock()  # Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize - 100, surfaceSize))

    # -----------------------------Program Variable Initialization----------------------------#
    #  game state
    gameState = "main game"

    #  main game state variables
    cardsBackground = pygame.image.load('cardGameBg.jpg')
    cardsBackground = pygame.transform.scale(cardsBackground, (surfaceSize, surfaceSize))
    #  Card variables
    cardsBack = pygame.image.load("card_back.png")
    cardsFront = pygame.image.load("card_front.png")
    cardsPos = [(50, 100), (200, 100), (350, 100), (500, 100), (650, 100), (50, 300), (200, 300), (350, 300),
                (500, 300),
                (650, 300), (50, 500), (200, 500), (350, 500), (500, 500), (650, 500), (50, 700), (200, 700),
                (350, 700), (500, 700), (650, 700)]
    cardFrontPos = [(-200, 0), (-200, 0)]
    numberOfCards = 20
    oneCardUp = False

    # -----------------------------Main Program Loop---------------------------------------------#
    while True:
        # -----------------------------Event Handling-----------------------------------------#

        ev = pygame.event.poll()  # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break  # ... leave game loop

        #  Makes the mouse click faster and run smoother because it doesn't consider the mouses motion or when there is
        #  no event
        if ev.type == pygame.MOUSEMOTION or ev.type == pygame.NOEVENT:
            continue

        if gameState == "main game":
            #  Event Handling
            #  Mouse position and click recognition
            if oneCardUp:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = ev.pos
                    for i in range(numberOfCards):
                        if cardsPos[i][0] <= mouseX <= cardsPos[i][0] + 100 and \
                                cardsPos[i][1] <= mouseY <= cardsPos[i][1] + 180:
                            cardFrontPos[1] = cardsPos[i]

            if not oneCardUp:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = ev.pos
                    for i in range(numberOfCards):
                        if cardsPos[i][0] <= mouseX <= cardsPos[i][0] + 100 and \
                                cardsPos[i][1] <= mouseY <= cardsPos[i][1] + 180:
                            print("card clicked")
                            cardFrontPos[0] = cardsPos[i]
                            oneCardUp = True

            # -----------------------------Program Logic---------------------------------------------#

            # -----------------------------Drawing Everything-------------------------------------#
            mainSurface.blit(cardsBackground, (0, 0))

            #  Drawing cards
            #  Back of card
            for i in range(numberOfCards):
                mainSurface.blit(cardsBack, cardsPos[i])
            #  Front of card
            mainSurface.blit(cardsFront, cardFrontPos[0])
            mainSurface.blit(cardsFront, cardFrontPos[1])
        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60)  # Force frame rate to be slower

    pygame.quit()  # Once we leave the loop, close the window.


main()
