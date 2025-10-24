import pygame
import config as Config


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player, level_data):
        # Center camera on player
        self.offset.x = player.rect.centerx - Config.WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - Config.WINDOW_HEIGHT / 2

        # Get level dimensions
        level_width = level_data.width * level_data.tilewidth
        level_height = level_data.height * level_data.tileheight

        # Clamp camera to level boundaries
        self.offset.x = max(0, min(self.offset.x, level_width - Config.WINDOW_WIDTH))
        self.offset.y = max(0, min(self.offset.y, level_height - Config.WINDOW_HEIGHT))

        # Draw all sprites with the calculated offset, sorting by layer then by y-coordinate
        for sprite in sorted(self.sprites(), key=lambda s: (getattr(s, 'layer', 0), s.rect.centery)):
            offset_rect = sprite.rect.copy()
            offset_rect.topleft -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)
