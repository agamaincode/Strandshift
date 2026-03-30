import pygame
from game.settings import sc, clock, fps, red, green, W, H, bottom_panel, BasicFont, BiggerFont
from game.ui.draw import draw_bg, draw_panel, draw_text
from game.ui.healthbar import HealthBar
from game.ui.button import Button

def battle(hero, bandit_list):
    panel = pygame.Rect((0, H-bottom_panel, W, bottom_panel))
    
    hero_health_bar = HealthBar(100, H-bottom_panel+40, hero.hp, hero.max_hp)
    bandit_health_bars = []
    for i, bandit in enumerate(bandit_list):
        y = H-bottom_panel+40 + i*60
        bandit_health_bars.append(HealthBar(550, y, bandit.hp, bandit.max_hp))

    current_fighter = 1
    total_fighters = 1 + len(bandit_list)
    action_cooldown = 0
    action_wait_time = 90
    clicked = False
    current_cursor = pygame.SYSTEM_CURSOR_ARROW

    fighting = True
    while fighting:
        draw_bg()
        draw_panel(panel, hero, bandit_list)

        hero_health_bar.draw(hero.hp)
        for i, bandit in enumerate(bandit_list):
            bandit_health_bars[i].draw(bandit.hp)

        hero.draw()
        for bandit in bandit_list:
            bandit.draw()

        # CONTROLS
        attack = False
        target = None
        pos = pygame.mouse.get_pos()

        new_cursor = pygame.SYSTEM_CURSOR_ARROW
        for count, bandit in enumerate(bandit_list):
            if bandit.alive and bandit.rect.collidepoint(pos):
                new_cursor = pygame.SYSTEM_CURSOR_CROSSHAIR
                if clicked:
                    attack = True
                    target = bandit

        if new_cursor != current_cursor:
            pygame.mouse.set_cursor(new_cursor)
            current_cursor = new_cursor

        # player action
        if hero.alive and current_fighter == 1:
            action_cooldown += 1
            if action_cooldown >= action_wait_time and attack and target:
                hero.attack(target)
                current_fighter += 1
                action_cooldown = 0
        
        # enemy action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count and bandit.alive:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    bandit.attack(hero)
                    current_fighter += 1
                    action_cooldown = 0

            elif current_fighter == 2 + count and not bandit.alive:
                current_fighter += 1

        if current_fighter > total_fighters:
            current_fighter = 1

        # checking for win or lose conditions
        if hero.hp <= 0:
            show_result("you lose", red)
            fighting = False
        if all(not bandit.alive for bandit in bandit_list):
            show_result("you win", green)
            fighting = False

        
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        pygame.display.update()
        clock.tick(fps)

def show_result(text, color):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    waiting = True
    while waiting:
        draw_bg()
        draw_text(text, BiggerFont, color, 325, 100)
        draw_text("click to continue", BasicFont, color, 325, 200)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        clock.tick(fps)
