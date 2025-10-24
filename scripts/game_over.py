import pygame
import config as Config


class GameOver:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.image = pygame.image.load(
            Config.PROPS_PATH + "gameover.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(
            center=(Config.WINDOW_WIDTH / 2, Config.WINDOW_HEIGHT / 2)
        )

        # Define clickable areas for the buttons on the sprite
        # Coords are based on the user's feedback
        self.quit_rect = pygame.Rect(434, 283, 30, 30)
        self.restart_rect = pygame.Rect(500, 283, 30, 30)

    def run(self):
        self.display_surface.blit(self.image, self.rect)

        # Draw green borders for visualization
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.quit_rect, 2)
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.restart_rect, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_rect.collidepoint(event.pos):
                    return "restart"
                if self.quit_rect.collidepoint(event.pos):
                    return "quit"
        return "game_over"
