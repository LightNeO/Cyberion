import pygame
import config as Config
from level import Level0, Level1, Level2
from hero import Hero
from game_over import GameOver
from pause import Pause


def main():
    # Init
    pygame.init()
    clock = pygame.time.Clock()
    displaySurface = pygame.display.set_mode(
        (Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)
    )
    pygame.display.set_caption("Cyberion")

    # Level setup
    levels = [Level0, Level1, Level2]
    level_index = 0
    level = levels[level_index](displaySurface)
    game_over_screen = GameOver(displaySurface)
    pause_screen = Pause(displaySurface)
    game_state = "playing"

    isGameRunning = True
    while isGameRunning:
        if game_state == "playing":
            for event in pygame.event.get():
                if level.quit:
                    isGameRunning = False
                if event.type == pygame.QUIT:
                    isGameRunning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "pause"

            should_change_level = level.run()
            if should_change_level:
                level_index += 1
                if level_index < len(levels):
                    level = levels[level_index](displaySurface)
                else:
                    print("Congratulations! You've completed DEMO.")
                    isGameRunning = False

            if Hero.get_hp() <= 0:
                game_state = "game_over"

        elif game_state == "game_over":
            result = game_over_screen.run()
            if result == "restart":
                Hero.change_hp(5)
                level = levels[0](displaySurface)
                Hero._bullets = 10
                level_index = 0
                game_state = "playing"
            elif result == "quit":
                isGameRunning = False
        
        elif game_state == "pause":
            result = pause_screen.run()
            if result == "resume":
                game_state = "playing"
            elif result == "restart":
                Hero.change_hp(5)
                level = levels[0](displaySurface)
                level_index = 0
                Hero._bullets = 10
                game_state = "playing"
            elif result == "quit":
                isGameRunning = False

        if isGameRunning:
            pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
