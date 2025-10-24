import pygame
import config as Config


class Background:
    def __init__(self):
        self.background = pygame.image.load(Config.SPRITESHEET_PATH + "environment/props/BG.png").convert()
        self.background = pygame.transform.scale(self.background, (Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))

    def draw(self, displaySurface):
        displaySurface.blit(self.background, (0, 0))
