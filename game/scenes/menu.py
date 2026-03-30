import pygame
from game.settings import sc, clock, fps, BiggerFont, white, green, red
from game.ui.button import Button
from game.ui.draw import draw_bg, draw_text
from game.scenes.battle import battle
from game.classes.hero import Hero

hero = Hero(150, 260, "Knight", 60, 20, 3)
bandit1 = Hero(550, 270, "Bandit", 40, 12, 1)
bandit2 = Hero(700, 270, "Bandit", 40, 12, 1)
bandit_list = [bandit1, bandit2]

def main_menu():
    start_button = Button(green, 280, 100, 200, 50, text="play")
    quit_button = Button(red, 280, 200, 200, 50, text="quit")

    in_menu = True
    while in_menu:
        draw_bg()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        start_button.draw()
        quit_button.draw()
        draw_text("Strandshift", BiggerFont, white, 300, 50)

        pos = pygame.mouse.get_pos()
        if start_button.isOver(pos) and clicked:
            battle(hero, bandit_list)
            hero.reset()
            for bandit in bandit_list:
                bandit.reset()

        if quit_button.isOver(pos) and clicked:
            pygame.quit()
            return

        pygame.display.update()
        clock.tick(fps)
