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
from controllers.state_manager import StateManager

logger = logging.getLogger(__name__)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spin The Wheel Game")
clock = pygame.time.Clock()

def main():
    """Main game loop.

    This function initializes and runs the game with state management.
    """
    config_manager = ConfigManager()
    state_manager = StateManager()
    menu_view = MenuView(screen)
    menu_controller = MenuController(menu_view)
    config_view = ConfigView(screen, config_manager.config)
    config_controller = ConfigController(config_view, config_manager, state_manager)
    game_state = GameStateTracker(len(config_manager.config["questions"]))
    game_view = GameView(screen, config_manager.config)
    game_controller = GameController(game_state, game_view, config_manager)

    state_manager.register_controller("menu", menu_controller)
    state_manager.register_controller("config", config_controller)
    state_manager.register_controller("game", game_controller)

    try:
        music_path = Path('assets') / 'backgrounds' / config_manager.config["music"]
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(-1)
    except (FileNotFoundError, pygame.error) as e:
        logger.error(f"Music loading error: {e}")

    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Game exited")
                pygame.quit()
                sys.exit()
            state_manager.handle_event(event)
        state_manager.update(dt)
        pygame.display.flip()

if __name__ == "__main__":
    main()