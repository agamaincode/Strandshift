import pygame
from game.settings import sc, gray, brown, BasicFont, red, H, bottom_panel

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    sc.blit(img, (x, y))

def draw_bg():
    sc.fill(gray)

def draw_panel(panel, hero, bandit_list):
    pygame.draw.rect(sc, brown, panel)
    draw_text(f'{hero.name} HP:{hero.hp}', BasicFont, red, 100, H-bottom_panel+10)
    for count, i in enumerate(bandit_list):
        draw_text(f'{i.name} HP: {i.hp}', BasicFont, red, 550, (H-bottom_panel+10)+count*60)

