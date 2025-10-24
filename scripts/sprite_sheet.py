import pygame


class SpriteSheet:
    def __init__(self, sprite_paths):
        self.sprites = []
        self.sprites_flipped = []
        for path in sprite_paths:
            sprite = pygame.image.load(path).convert_alpha()
            self.sprites.append(sprite)
            flipped_sprite = pygame.transform.flip(sprite, True, False)
            self.sprites_flipped.append(flipped_sprite)

    def get_sprites(self, flipped):
        if not flipped:
            return self.sprites_flipped
        else:
            return self.sprites


