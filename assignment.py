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

    #  counter of amount of clicks
    counter = pygame.font.SysFont('impact', 45)
    clickCount = 0

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
                    visible[selectedCard] = False
                    visible[selectedCard2] = False
                    sideUp[selectedCard] = False
                    sideUp[selectedCard2] = False

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
                        mainSurface.blit(sprites[i][0], (cardsPos[i][0]+20, cardsPos[i][1]+30))

            #  Click counter
            clickText = counter.render(f"Clicks: {clickCount}", False, (255, 255, 255))
            mainSurface.blit(clickText, (10, 10))

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60)  # Force frame rate to be slower

    pygame.quit()  # Once we leave the loop, close the window.


main()
