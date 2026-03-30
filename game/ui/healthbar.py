import pygame
from game.settings import sc, red, green

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        self.hp = hp
        ratio = self.hp/self.max_hp
        pygame.draw.rect(sc, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(sc, green, (self.x, self.y, 150* ratio, 20))
