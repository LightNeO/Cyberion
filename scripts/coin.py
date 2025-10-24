import pygame
import config as Config


class Coin(pygame.sprite.Sprite):
    def __init__(self, position, surface):
        super().__init__()
        self.layer = Config.LAYER_MAIN
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
