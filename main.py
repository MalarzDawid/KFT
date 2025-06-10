import pygame
import sys
import logging

from pathlib import Path
from constants import WIDTH, HEIGHT, FPS
from models.logger import GameStateTracker
from models.config_manager import ConfigManager
from views.game_view import GameView
from views.config_view import ConfigView
from views.menu_view import MenuView
from controllers.game_controller import GameController
from controllers.config_controller import ConfigController
from controllers.menu_controller import MenuController

logger = logging.getLogger(__name__)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spin The Wheel Game")
clock = pygame.time.Clock()

def main():
    """Main game loop."""
    config_manager = ConfigManager()
    state = "menu"
    menu_view = MenuView(screen)
    menu_controller = MenuController(menu_view)
    config_view = ConfigView(screen, config_manager.config)
    config_controller = ConfigController(config_view, config_manager)
    game_controller = None

    try:
        music_path = Path('assets') / 'backgrounds' / config_manager.config["music"]
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(-1)
    except FileNotFoundError:
        logger.error(f"Music file not found: {music_path}")
    except pygame.error as e:
        logger.error(f"Error loading music: {e}")

    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Game exited")
                pygame.quit()
                sys.exit()
            if state == "menu":
                action = menu_controller.handle_event(event)
                if action == "configure":
                    config_controller.go_back = False
                    config_controller.done = False
                    state = "config"
                    logger.info("Switched to config state")
                elif action == "play":
                    game_state = GameStateTracker(len(config_manager.config["questions"]))
                    game_view = GameView(screen, config_manager.config)
                    game_controller = GameController(game_state, game_view, config_manager)
                    game_controller.wheel.spin()
                    state = "game"
                    logger.info("Switched to game state")
            elif state == "config":
                config_controller.handle_event(event)
                if config_controller.go_back:
                    state = "menu"
                    logger.info("Returned to menu state")
                elif config_controller.done:
                    state = "menu"
                    logger.info("Configuration saved, returned to menu")
            elif state == "game":
                game_controller.handle_event(event)

        if state == "menu":
            menu_controller.update()
        elif state == "config":
            config_controller.update()
        elif state == "game":
            game_controller.update(dt)

        pygame.display.flip()

if __name__ == "__main__":
    main()