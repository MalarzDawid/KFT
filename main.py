import pygame
import sys
from constants import WIDTH, HEIGHT, FPS
from menu import Menu
from config import ConfigScreen
from app import MultipleDrawsApp  # Your existing game logic
import os

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spin Wheel Game")
clock = pygame.time.Clock()



MENU, CONFIG, GAME = "menu", "config", "game"

def main():
    state = MENU
    config = ConfigScreen(screen)
    menu = Menu(screen)
    app = None

    running = True
    try:
        pygame.mixer.music.load(os.path.join('assets','backgrounds', config.get_config()["music"]))
        pygame.mixer.music.set_volume(0.01)
        pygame.mixer.music.play(-1)
    except:
        pass

    while running:
        
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == MENU:
                action = menu.handle_event(event)
                if action == "configure":
                    config.go_back = False
                    config.done = False
                    state = CONFIG
                elif action == "play":
                    app = MultipleDrawsApp(screen, config=config.get_config())
                    app.wheel.spin()
                    state = GAME
            elif state == CONFIG:
                config.handle_event(event)
                if config.go_back:
                    state = MENU
                elif config.done:
                    game_config = config.get_config()
                    print("Saved Config:", game_config)  # or send to GPT here
                    state = MENU


            elif state == GAME:
                app.handle_event(event)

        if state == MENU:
            menu.update(dt)
            menu.draw()
        elif state == CONFIG:
            config.update(dt)
            config.draw()
        elif state == GAME:
            app.update(dt)
            app.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
