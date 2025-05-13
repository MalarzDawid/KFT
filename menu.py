import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)
        self.buttons = [
            {"label": "Configure Game", "pos": (600, 250), "action": "configure"},
            {"label": "Play Game", "pos": (600, 350), "action": "play"},
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for button in self.buttons:
                rect = pygame.Rect(button["pos"][0] - 100, button["pos"][1] - 25, 200, 50)
                if rect.collidepoint(x, y):
                    return button["action"]
        return None

    def update(self, dt): pass

    def draw(self):
        self.screen.fill((30, 30, 30))
        for button in self.buttons:
            rect = pygame.Rect(button["pos"][0] - 100, button["pos"][1] - 25, 200, 50)
            pygame.draw.rect(self.screen, (70, 70, 70), rect)
            label = self.font.render(button["label"], True, (255, 255, 255))
            self.screen.blit(label, (button["pos"][0] - label.get_width()//2, button["pos"][1] - label.get_height()//2))
