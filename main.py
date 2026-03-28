import pygame
import random
pygame.init()

bottom_panel = 150
W, H = 800, 400+bottom_panel # screen width and height
sc = pygame.display.set_mode((W, H))

pygame.display.set_caption("Strandshift")

# FONTS
font = pygame.font.SysFont('Times New Roman', 24)
bigger_font = pygame.font.SysFont('Times New Roman', 36)

#define colors
red = (255, 0, 0)
green = (0, 255, 0)

# LOAD IMAGES HERE

# TODO draw and add textures
# pygame.display.set_icon(pygame.image.load("imgs/icon.png"))
# menubg = pygame.image.load("imgs/menubg.png")
# forestbg = pygame.image.load("imgs/battlebg.png")
# panel_img = pygame.image.load("imgs/panel.png")


clock = pygame.time.Clock()
fps = 60


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    sc.blit(img, (x, y))

def draw_bg():
    sc.fill((40, 40, 40)) # TODO change to an image background

def draw_panel(panel):
    #draw panel
    pygame.draw.rect(sc, (107, 67, 27), panel)
    #draw hero stats
    draw_text(f'{hero.name} HP: {hero.hp}', font, red, 100, H-bottom_panel+10)
    for count, i in enumerate(bandit_list):
        draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (H-bottom_panel+10) + count*60)



class Button():
    def __init__(self, color, x, y, width, height, text=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self):
        pygame.draw.rect(sc, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('Times New Roman', 24)
            text = font.render(self.text, 1, (0, 0, 0))
            sc.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

class Hero():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        # TODO add animations
        self.image = pygame.image.load(f'imgs/{self.name}.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        sc.blit(self.image, self.rect)
    
    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        
        if target.hp < 1:
            target.hp = 0
            target.alive = False

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp



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
        pygame.draw.rect(sc, green, (self.x, self.y, 150 * ratio, 20))

# hero and enemies
hero = Hero(150, 260, "Knight", 60, 20, 3)
bandit1 = Hero(550, 270, "Bandit", 40, 12, 1)
bandit2 = Hero(700, 270, "Bandit", 40, 12, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

hero_health_bar = HealthBar(100, H-bottom_panel+40, hero.hp, hero.max_hp)
bandit1_health_bar = HealthBar(550, H-bottom_panel+40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, H-bottom_panel+100, bandit2.hp, bandit2.max_hp)

#buttons
main_menu_start_button = Button(green, 280, 100, 200, 50, text="play")
main_menu_quit_button = Button(red, 280, 200, 200, 50, text="quit")
level_selection_start_button = Button(green, 280, 400, 200, 50, text="play next")

def main_menu():
    in_menu = 1
    while in_menu:
        draw_bg()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
        main_menu_start_button.draw()
        main_menu_quit_button.draw()
        draw_text("Strandshift", bigger_font, (255, 255, 255), 300, 50)
        pos = pygame.mouse.get_pos()
        if main_menu_start_button.isOver(pos):
            if clicked:
                game()
                hero.reset()
                for bandit in bandit_list:
                    bandit.reset()

        if main_menu_quit_button.isOver(pos):
            if clicked:
                pygame.QUIT()
        pygame.display.update()
        clock.tick(fps)

def level_selection():
    print("selecting the level...")
    # TODO add levels ASAP
    return "fight"

def game(): # main game
    running = True
    panel = pygame.Rect((0, H-bottom_panel, W, bottom_panel))
    #game variables
    current_fighter = 1
    total_fighters = 3
    action_cooldown = 0
    action_wait_time = 90
    attack = False
    potion = False
    clicked = False
    game_over = 0
    next_level = level_selection()

    while running:
        if next_level == "menu":
            running = 0
        if next_level == "fight":
            fighting = True
            while fighting:
                draw_bg()

                draw_panel(panel)
                hero_health_bar.draw(hero.hp)
                bandit1_health_bar.draw(bandit1.hp)
                bandit2_health_bar.draw(bandit2.hp)

                hero.draw()
                for bandit in bandit_list:
                    bandit.draw()

                #control player actions
                attack = False
                potion = False
                target = None
                pos = pygame.mouse.get_pos()
                cursor = pygame.SYSTEM_CURSOR_ARROW
                for count, bandit in enumerate(bandit_list):
                    if bandit.rect.collidepoint(pos):
                        cursor = pygame.SYSTEM_CURSOR_CROSSHAIR
                        if clicked:
                            attack = True
                            target = bandit_list[count]
                pygame.mouse.set_cursor(cursor)        
                #player action
                if hero.alive:
                    if current_fighter == 1:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                            #attack
                            if attack == True and target != None:
                                hero.attack(target)
                                current_fighter += 1
                                action_cooldown = 0
                else:
                    game_over = -1
                    waiting_for_action = True
                    next_level = "menu"
                    fighting = False
                    while waiting_for_action:

                        for event in pygame.event.get():
                            draw_bg()
                            draw_text("you lose", bigger_font, red, 325, 100)
                            draw_text("click to contiune", font, red, 325, 200)
                            if event.type == pygame.QUIT:
                                running = False
                                waiting_for_action = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                waiting_for_action = False
                        
                        pygame.display.update()
                        clock.tick(fps)


                #enemy action
                for count, bandit in enumerate(bandit_list):
                    if current_fighter == 2 + count:
                        if bandit.alive == True:
                            action_cooldown += 1
                            if action_cooldown >= action_wait_time:
                                #attack
                                bandit.attack(hero)
                                current_fighter += 1
                                action_cooldown = 0
                        else:
                            current_fighter += 1

                if current_fighter > total_fighters:
                    current_fighter = 1

                #check if all bandits are dead
                alive_bandits = 0
                for bandit in bandit_list:
                    if bandit.alive == True:
                        alive_bandits += 1


                if alive_bandits == 0:
                    game_over = 1
                    fighting = False
                    waiting_for_action = True
                    while waiting_for_action:

                        for event in pygame.event.get():
                            draw_bg()
                            draw_text("you win", bigger_font, green, 325, 100)
                            draw_text("click to contiune", font, green, 325, 200)
                            if event.type == pygame.QUIT:
                                running = False
                                waiting_for_action = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                waiting_for_action = False
                        
                        pygame.display.update()
                        clock.tick(fps)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        fighting = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clicked = True
                    else:
                        clicked = False

                pygame.display.update()
                clock.tick(fps)
            next_level = "menu"

if __name__ == "__main__":
    main_menu()
