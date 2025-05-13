import pygame
import json
import os
from gpt import get_ai_request, create_prompt, AnswersModel
from constants import QUESTIONS, CONFIG_PATH


class ModernInputBox:
    def __init__(self, x, y, w, h, text='', numeric=False, label='', placeholder=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color(70, 70, 90)
        self.color_active = pygame.Color(100, 140, 230)
        self.color = self.color_inactive
        # Always store text as string, even for numeric fields
        self.text = str(text) if text is not None else ''
        self.label = label
        self.placeholder = placeholder
        self.font = pygame.font.SysFont("Arial", 20)
        self.label_font = pygame.font.SysFont("Arial", 18)
        self.txt_surface = self.font.render(self.text if self.text else placeholder, True, 
                                           pygame.Color('white') if self.text else pygame.Color(150, 150, 170))
        self.active = False
        self.numeric = numeric
        self.padding = 10
        self.bg_color = pygame.Color(50, 50, 70)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked on the input box
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_inactive
        
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
            else:
                # For numeric fields, only allow digits
                if self.numeric:
                    if event.unicode.isdigit():
                        self.text += event.unicode
                else:
                    # For text fields, allow any character
                    self.text += event.unicode
            
            # Update rendered text
            if self.text:
                self.txt_surface = self.font.render(self.text, True, pygame.Color('white'))
            else:
                self.txt_surface = self.font.render(self.placeholder, True, pygame.Color(150, 150, 170))

    def draw(self, screen):
        # Draw label if present
        if self.label:
            label_surface = self.label_font.render(self.label, True, pygame.Color(200, 200, 220))
            screen.blit(label_surface, (self.rect.x, self.rect.y - 25))
        
        # Draw input box background
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=4)
        
        # Draw border (thicker when active)
        border_thickness = 2 if self.active else 1
        pygame.draw.rect(screen, self.color, self.rect, border_thickness, border_radius=4)
        
        # Text positioning with padding
        screen.blit(self.txt_surface, (self.rect.x + self.padding, self.rect.y + (self.rect.height - self.txt_surface.get_height()) // 2))

    def get_value(self):
        return int(self.text) if self.numeric and self.text.isdigit() else self.text


class ModernColorPicker:
    def __init__(self, x, y, colors, label=''):
        self.colors = colors
        self.rects = []
        self.selected_color = colors[0]
        self.label = label
        self.label_font = pygame.font.SysFont("Arial", 18)
        
        for i, color in enumerate(colors):
            rect = pygame.Rect(x + i * 45, y, 35, 35)
            self.rects.append((rect, color))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for rect, color in self.rects:
                if rect.collidepoint(event.pos):
                    self.selected_color = color
                    return
    
    def draw(self, screen):
        # Draw label if present
        if self.label:
            label_surface = self.label_font.render(self.label, True, pygame.Color(200, 200, 220))
            screen.blit(label_surface, (self.rects[0][0].x, self.rects[0][0].y - 25))
        
        for rect, color in self.rects:
            # Draw color swatch with rounded corners
            pygame.draw.rect(screen, color, rect, border_radius=5)
            
            # Draw border around selected color
            if color == self.selected_color:
                pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=5)
                # Draw checkmark
                check_x = rect.centerx - 7
                check_y = rect.centery - 3
                pygame.draw.line(screen, (255, 255, 255), (check_x, check_y), (check_x + 5, check_y + 5), 2)
                pygame.draw.line(screen, (255, 255, 255), (check_x + 5, check_y + 5), (check_x + 12, check_y - 7), 2)


class ModernButton:
    def __init__(self, x, y, w, h, text, color=(70, 120, 200), hover_color=(100, 150, 230)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.text = text
        self.font = pygame.font.SysFont("Arial", 22)
        self.text_surface = self.font.render(text, True, pygame.Color('white'))
        self.is_hovered = False
        
    def handle_event(self, event, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.is_hovered else self.color
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            return True
        return False
        
    def draw(self, screen):
        # Draw button with rounded corners
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=6)
        
        # Draw text centered
        screen.blit(self.text_surface, (
            self.rect.centerx - self.text_surface.get_width() // 2,
            self.rect.centery - self.text_surface.get_height() // 2
        ))


class ConfigScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.tiny_font = pygame.font.SysFont("Arial", 16)
        self.done = False
        self.go_back = False
        
        # Set colors
        self.bg_color = (30, 30, 45)
        self.panel_color = (40, 40, 60)
        self.accent_color = (70, 120, 200)
        
        # Create buttons
        self.save_button = ModernButton(550, 600, 180, 50, "Zapisz i Generuj", (60, 180, 100), (80, 210, 120))
        self.back_button = ModernButton(50, 600, 150, 50, "Powrót", (180, 70, 70), (210, 90, 90))
        
        # Universe prompt input
        self.prompt_box = ModernInputBox(250, 70, 460, 40, "Star Wars", label="Uniwersum:", placeholder="Podaj nazwę uniwersum...")
        
        # Background color picker
        self.color_picker = ModernColorPicker(800, 230, [
            (30, 30, 60),  # Dark blue
            (60, 30, 60),  # Purple
            (30, 60, 30),  # Dark green
            (60, 30, 30),  # Dark red
            (30, 30, 30),  # Dark gray
            (60, 60, 30)   # Dark yellow
        ], label="Kolor tła:")

        # Music file input
        self.music_box = ModernInputBox(800, 310, 360, 40, "music.mp3", label="Plik muzyczny:", placeholder="Podaj nazwę pliku...")

        # Inputs for number of answers
        self.answer_inputs = []
        for i in range(len(QUESTIONS)):
            y = 150 + i * 45
            input_box = ModernInputBox(650, y, 60, 35, "5", numeric=True)
            self.answer_inputs.append(input_box)
            
        # Load existing config if available
        self.load_config()

    def get_config(self):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data    

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                if "prompt" in data:
                    self.prompt_box.text = str(data["prompt"])
                    self.prompt_box.txt_surface = self.prompt_box.font.render(
                        self.prompt_box.text, True, pygame.Color('white')
                    )
                
                if "music" in data:
                    self.music_box.text = str(data["music"])
                    self.music_box.txt_surface = self.music_box.font.render(
                        self.music_box.text, True, pygame.Color('white')
                    )
                
                if "bg_color" in data:
                    for rect, color in self.color_picker.rects:
                        if color == tuple(data["bg_color"]):
                            self.color_picker.selected_color = color
                
                if "questions" in data:
                    for i, q_data in enumerate(data["questions"]):
                        if i < len(self.answer_inputs):
                            self.answer_inputs[i].text = str(q_data.get("num_answers", 5))
                            self.answer_inputs[i].txt_surface = self.answer_inputs[i].font.render(
                                self.answer_inputs[i].text, True, pygame.Color('white')
                            )
            except Exception as e:
                print(f"Error loading config: {e}")
                # Will use default values

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.save_button.handle_event(event, mouse_pos):
            self.ai()
            self.save_to_file()
            self.done = True
            return
            
        if self.back_button.handle_event(event, mouse_pos):
            self.go_back = True
            return

        # Handle inputs
        self.prompt_box.handle_event(event)
        self.music_box.handle_event(event)
        self.color_picker.handle_event(event)
        
        for answer_input in self.answer_inputs:
            answer_input.handle_event(event)

    def update(self, dt):
        pass

    def draw(self):
        # Draw background
        self.screen.fill(self.bg_color)
        
        # Draw main panel
        main_panel = pygame.Rect(40, 40, 720, 550)
        pygame.draw.rect(self.screen, self.panel_color, main_panel, border_radius=10)
        pygame.draw.rect(self.screen, (60, 60, 80), main_panel, 2, border_radius=10)
        
        # Title
        title = self.font.render("Konfiguracja Gry", True, pygame.Color('white'))
        self.screen.blit(title, (400 - title.get_width() // 2, 20))
        
        # Draw universe prompt input
        self.prompt_box.draw(self.screen)
        
        # Questions section
        questions_rect = pygame.Rect(70, 130, 660, 220)
        pygame.draw.rect(self.screen, (45, 45, 65), questions_rect, border_radius=6)
        
        # Header for questions
        q_header = self.small_font.render("Pytania i liczba odpowiedzi", True, pygame.Color(220, 220, 240))
        self.screen.blit(q_header, (questions_rect.centerx - q_header.get_width() // 2, 135))
        
        # Draw questions and answer inputs
        for i, text in enumerate(QUESTIONS):
            y = 150 + i * 45
            q_label = self.small_font.render(f"{i+1}. {text}", True, pygame.Color('white'))
            
            # Draw question number in a circle
            circle_pos = (90, y + 12)
            pygame.draw.circle(self.screen, self.accent_color, circle_pos, 15)
            num_label = self.small_font.render(f"{i+1}", True, pygame.Color('white'))
            self.screen.blit(num_label, (circle_pos[0] - num_label.get_width() // 2, 
                                         circle_pos[1] - num_label.get_height() // 2))
            
            # Draw question text
            self.screen.blit(q_label, (120, y))
            
            # Draw answer input field
            input_rect = self.answer_inputs[i].rect.copy()
            input_rect.y = y
            self.answer_inputs[i].rect = input_rect
            self.answer_inputs[i].draw(self.screen)
        
        # Draw color picker
        self.color_picker.draw(self.screen)
        
        # Draw music file input
        self.music_box.draw(self.screen)
        
        # Draw buttons
        self.save_button.draw(self.screen)
        self.back_button.draw(self.screen)
            
        # AI Prompt preview section
        ai_prompt = f'Jesteś twórcą wideo w stylu "Spin the wheel". Odpowiadasz na poniższe pytania, korzystając wyłącznie z uniwersum {self.prompt_box.text}. Odpowiadaj tylko w formacie JSON, bez żadnych wyjaśnień, opisów czy dodatkowych komentarzy.'
        
        # Draw AI prompt preview
        prompt_panel = pygame.Rect(40, 660, 720, 90)
        pygame.draw.rect(self.screen, (45, 45, 65), prompt_panel, border_radius=6)
        
        # Label for prompt preview
        preview_label = self.small_font.render("Podgląd zapytania AI", True, pygame.Color(220, 220, 240))
        self.screen.blit(preview_label, (prompt_panel.x + 10, prompt_panel.y + 5))
        
        # Render multi-line prompt text
        words = ai_prompt.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if self.tiny_font.size(test_line)[0] < 700:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
            
        for i, line in enumerate(lines):
            prompt_text = self.tiny_font.render(line, True, pygame.Color(200, 200, 220))
            self.screen.blit(prompt_text, (prompt_panel.x + 10, prompt_panel.y + 30 + i * 20))

    def save_to_file(self):
        data = {
            "prompt": self.prompt_box.get_value(),
            "music": self.music_box.get_value(),
            "bg_color": list(self.color_picker.selected_color),
            "questions": [
                {"text": question, 
                 "num_answers": num_answers.get_value()}
                for question, num_answers in zip(QUESTIONS, self.answer_inputs)
            ]
        }

        if hasattr(self, 'answers'):
            # Add AI-generated answers to the configuration
            for i, (field_name, question_data) in enumerate(zip(self.answers.model_dump().keys(), data["questions"])):
                question_data["answers"] = self.answers.__getattribute__(field_name)

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Configuration saved to {CONFIG_PATH}")

    def ai(self):
        universe = self.prompt_box.get_value()
        prompt = create_prompt(universe)
        self.answers = get_ai_request(prompt)