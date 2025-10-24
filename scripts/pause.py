import pygame
import config as Config


class Pause:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.image = pygame.image.load(
            Config.PROPS_PATH + "pause.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(
            center=(Config.WINDOW_WIDTH / 2, Config.WINDOW_HEIGHT / 2)
        )

        # Define clickable areas for the buttons on the sprite
        # Coords are based on the user's feedback
        self.quit_rect = pygame.Rect(418, 266, 30, 30)
        self.restart_rect = pygame.Rect(514, 266, 30, 30)
        self.resume_rect = pygame.Rect(466, 266, 30, 30)

    def run(self):
        self.display_surface.blit(self.image, self.rect)

        # Draw green borders for visualization
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.quit_rect, 2)
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.restart_rect, 2)
        pygame.draw.rect(self.display_surface, (0, 255, 0), self.resume_rect, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_rect.collidepoint(event.pos):
                    return "restart"
                if self.quit_rect.collidepoint(event.pos):
                    return "quit"
                if self.resume_rect.collidepoint(event.pos):
                    return "resume"
        return "pause"
