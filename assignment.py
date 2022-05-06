# -----------------------------------------------------------------------------
# Name:        Match and Snatch
# Purpose:     A description of your program goes here.
#
# Author:      Mr. Brooks
# Created:     13-Sept-2020
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


def main():
    # -----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()  # Prepare the pygame module for use
    surfaceSize = 800  # Desired physical surface size, in pixels.

    clock = pygame.time.Clock()  # Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    # -----------------------------Program Variable Initialization----------------------------#
    #  game state
    gameState = "main game"

    #  Card variables
    cardsBack = pygame.image.load("card_back.png")
    cardsPos = [(50, 20), (200, 20), (350, 20), (500, 20), (650, 20), (50, 220)]
    numberOfCards = 6

    # -----------------------------Main Program Loop---------------------------------------------#
    while True:
        # -----------------------------Event Handling-----------------------------------------#
        ev = pygame.event.poll()  # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break  # ... leave game loop

        if gameState == "main game":
            # -----------------------------Program Logic---------------------------------------------#

            # -----------------------------Drawing Everything-------------------------------------#
            mainSurface.fill((0, 200, 255))

            #  Drawing cards
            for i in range(numberOfCards):
                mainSurface.blit(cardsBack, cardsPos[i])

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60)  # Force frame rate to be slower

    pygame.quit()  # Once we leave the loop, close the window.


main()
