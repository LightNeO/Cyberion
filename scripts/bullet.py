import pygame
import config as Config


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, move_right, bullet_type="hero"):
        super().__init__()
        self.layer = Config.LAYER_MAIN
        self.bullet_type = bullet_type
        sprite_paths = [
            Config.SPRITESHEET_PATH + "sprites/misc/shot/shot-1.png",
            Config.SPRITESHEET_PATH + "sprites/misc/shot/shot-2.png",
            Config.SPRITESHEET_PATH + "sprites/misc/shot/shot-3.png",
        ]
        self.images = [pygame.image.load(p).convert_alpha() for p in sprite_paths]
        self.animation_index = 0.0
        self.image = self.images[0]
        if not move_right:
            self.images = [
                pygame.transform.flip(img, True, False) for img in self.images
            ]
        self.rect = self.image.get_rect(center=position)
        self.move_right = move_right

    def update(self, level):
        dx = Config.BULLET_SPEED if self.move_right else -Config.BULLET_SPEED
        self.rect.x += dx
        # Animate
        self.animation_index += Config.BULLET_ANIMATION_SPEED
        if self.animation_index >= len(self.images):
            self.animation_index = 0.0
        self.image = self.images[int(self.animation_index)]

        # Remove bullets that are far offscreen (considering level bounds and camera)
        level_width = level.level_data.width * level.level_data.tilewidth
        # Remove bullets that are way off the level bounds
        if self.rect.right < -100 or self.rect.left > level_width + 100:
            self.kill()
