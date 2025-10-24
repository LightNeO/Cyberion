import pygame
import config as Config


class UI:
    def __init__(self, surface):
        self.display_surface = surface
        self.font = pygame.font.Font(None, 30)
        self.coin_image = pygame.image.load(Config.SPRITESHEET_PATH + 'environment/props/coin.png').convert_alpha()
        self.bullet_image = pygame.image.load(Config.SPRITESHEET_PATH + 'sprites/misc/shot/shot-1.png').convert_alpha()
        self.hp_image = pygame.image.load(Config.SPRITESHEET_PATH + 'environment/props/hp.png').convert_alpha()
        self.coin_rect = self.coin_image.get_rect(topleft=(20, 20))
        self.bullet_rect = self.bullet_image.get_rect(topleft=(60, 19))
        self.hp_rect = self.hp_image.get_rect(topleft=(120, 17))

    def show_coins(self, amount):
        self.display_surface.blit(self.coin_image, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, "#ffffff")
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)

    def show_hp(self, amount):
        self.display_surface.blit(self.hp_image, self.hp_rect)
        hp_amount_surf = self.font.render(str(amount), False, "#ffffff")
        hp_amount_rect = hp_amount_surf.get_rect(midleft=(self.hp_rect.right + 4, self.hp_rect.centery))
        self.display_surface.blit(hp_amount_surf, hp_amount_rect)

    def show_bullets(self, amount):
        self.display_surface.blit(self.bullet_image, self.bullet_rect)
        bullet_amount_surf = self.font.render(str(amount), False, "#ffffff")
        bullet_amount_rect = bullet_amount_surf.get_rect(midleft=(self.bullet_rect.right + 4, self.bullet_rect.centery))
        self.display_surface.blit(bullet_amount_surf, bullet_amount_rect)
