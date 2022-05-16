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

    numberOfCards = 20
    #  Makes all the cards back visible and all card fronts invisible
    visible = [True for _ in range(numberOfCards)]
    sideUp = [False for _ in range(numberOfCards)]

    selectedCard2 = -1
    selectedCard = -1

    oneCardUp = False
    upTime = 0
    secondCardUp = False
    #  Sprites
    demon = pygame.image.load('big_demon_idle_anim_f0.png')
    doubledDemon = pygame.transform.scale2x(demon)
    zombie = pygame.image.load('big_zombie_idle_anim_f0.png')
    doubledZombie = pygame.transform.scale2x(zombie)
    elf = pygame.image.load('elf_m_hit_anim_f0.png')
    doubleElf = pygame.transform.scale2x(elf)
    flask = pygame.image.load('flask_big_blue.png')
    doubleFlask = pygame.transform.scale2x(flask)
    goblin = pygame.image.load('goblin_idle_anim_f0.png')
    doubledGoblin = pygame.transform.scale2x(goblin)
    iceZombie = pygame.image.load('ice_zombie_run_anim_f0.png')
    doubleIceZombie = pygame.transform.scale2x(iceZombie)
    knight = pygame.image.load('knight_f_hit_anim_f0.png')
    doubledKnight = pygame.transform.scale2x(knight)
    lizard = pygame.image.load('lizard_m_idle_anim_f1.png')
    doubleLizard = pygame.transform.scale2x(lizard)
    swampy = pygame.image.load('swampy_idle_anim_f1.png')
    doubledSwampy = pygame.transform.scale2x(swampy)
    wizzard = pygame.image.load('wizzard_m_idle_anim_f1.png')
    doubledWizzard = pygame.transform.scale2x(wizzard)

    # -----------------------------Main Program Loop---------------------------------------------#
    while True:
        # -----------------------------Event Handling-----------------------------------------#

        ev = pygame.event.poll()  # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break  # ... leave game loop

        #  Makes the mouse click faster and run smoother because it doesn't consider the mouses motion or when there is
        #  no event
        if ev.type == pygame.MOUSEMOTION:
            continue

        if gameState == "main game":

            #  Event Handling
            #  Mouse position and click recognition
            if oneCardUp:
                if ev.type == pygame.MOUSEBUTTONDOWN and not secondCardUp:
                    mouseX, mouseY = ev.pos
                    for i in range(numberOfCards):
                        if i != selectedCard and cardsPos[i][0] <= mouseX <= cardsPos[i][0] + 100 and \
                                cardsPos[i][1] <= mouseY <= cardsPos[i][1] + 180:
                            selectedCard2 = i
                            upTime = pygame.time.get_ticks()
                            secondCardUp = True
                            sideUp[i] = True
                            break

                currentTime = pygame.time.get_ticks()
                if upTime > 0 and currentTime - upTime > 1000:
                    sideUp[selectedCard] = False
                    sideUp[selectedCard2] = False
                    selectedCard2 = False
                    oneCardUp = False
                    upTime = 0
                    secondCardUp = False

            elif not oneCardUp:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = ev.pos
                    for i in range(numberOfCards):
                        if cardsPos[i][0] <= mouseX <= cardsPos[i][0] + 100 and \
                                cardsPos[i][1] <= mouseY <= cardsPos[i][1] + 180:
                            print("card clicked")
                            oneCardUp = True
                            selectedCard = i
                            sideUp[i] = True
                            break

            # -----------------------------Program Logic---------------------------------------------#

            # -----------------------------Drawing Everything-------------------------------------#
            mainSurface.blit(cardsBackground, (0, 0))

            #  Drawing cards
            #  Back of card
            for i in range(numberOfCards):
                if visible[i]:
                    cardImage = cardsBack
                    if sideUp[i]:  # Front of card
                        cardImage = cardsFront
                    mainSurface.blit(cardImage, cardsPos[i])

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60)  # Force frame rate to be slower

    pygame.quit()  # Once we leave the loop, close the window.


main()
