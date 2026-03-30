import random
import pygame
from game.settings import sc

class Hero():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.image = pygame.image.load(f'imgs/{self.name}.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        sc.blit(self.image, self.rect)

    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength+rand
        target.hp -= damage

        if target.hp < 1:
            target.hp = 0
            target.alive = False

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
