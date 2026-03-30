import pygame

pygame.init()

# SCREEN
bottom_panel = 150
W, H = 800, 400+bottom_panel
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Strandshift")

# CLOCK
clock = pygame.time.Clock()
fps = 60


# FONTS
BasicFont = pygame.font.SysFont('Times New Roman', 24)
BiggerFont = pygame.font.SysFont('Times New Roman', 36)


# COLORS
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
gray = (40, 40, 40)
brown = (107, 67, 27)
black = (0, 0, 0)
