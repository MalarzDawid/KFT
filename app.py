import pygame
from pygame import gfxdraw
import os
from spin_wheel import SpinWheel
from constants import WIDTH, HEIGHT, FONT_SIZE, QUESTIONS
import imageio.v2 as imageio  # Added for GIF loading
import json
import random
import codecs
import sys

class MultipleDrawsApp:
    def __init__(self, screen, config):
        self.screen = screen
        self.isresultsaved = False
        self.config = config
        self.total_draws = len(self.config["questions"])
        self.current_draw = 0
        self.results = []
        self.result_responses = []  # Store the selected responses
        self.generate_new_wheel()
        self.state = "spinning"  # States: spinning, waiting, results, showing_gif
        self.wait_timer = 0
        self.font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)
        self.response_font = pygame.font.SysFont("Arial", int(FONT_SIZE * 0.8))  # Slightly smaller font for responses
        self.gif_frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 0.1  # 100ms between frames
        self.responses = self.load_response("TextResp.json")
        self.small_font = pygame.font.SysFont("Arial", int(FONT_SIZE * 0.7), bold=True)  # Smaller font

    
    def load_response(self, filename):
        with open(filename, "r") as f:
            data = json.load(codecs.open(filename, 'r', 'utf-8-sig'))
        return data
    
    def generate_new_wheel(self):
        # Generate a random number of segments between 4 and 8
        data = self.config["questions"][self.current_draw]

        # Generate unique prizes using OpenAI API
        choices = data["answers"][:data["num_answers"]]
        
        # Create a new wheel with these segments
        self.wheel = SpinWheel(choices)
        
    def load_gif(self, result):
        """Load the GIF directly without requiring separate frame files"""
        self.gif_frames = []
        self.current_frame = 0
        
        # Convert result to a filename format
        safe_result = str(result)
        gif_path = os.path.join('assets','gifs',f"{safe_result}.gif")
        
        # Check if the GIF exists
        if not os.path.exists(gif_path):
            print(f"GIF not found: {gif_path}")
            return False
            
        try:
            # Use imageio to read the GIF file directly
            gif_reader = imageio.get_reader(gif_path)
            
            # Calculate frame delay from GIF metadata if available
            try:
                # Try to get the frame durations
                self.frame_delay = gif_reader.get_meta_data()['duration'] / 1000.0  # Convert ms to seconds
            except:
                # Default to 100ms if not specified
                self.frame_delay = 0.1
            
            # Convert each frame to a pygame surface
            for frame_idx in range(gif_reader.get_length()):
                frame_data = gif_reader.get_data(frame_idx)
                frame_surface = pygame.image.frombuffer(
                    frame_data.tobytes(), frame_data.shape[1::-1], "RGB")
                
                # Scale the frame to fit the screen if needed
                scale_factor = min(WIDTH / frame_surface.get_width(), HEIGHT / frame_surface.get_height()) * 0.8
                new_size = (int(frame_surface.get_width() * scale_factor), int(frame_surface.get_height() * scale_factor))
                frame_surface = pygame.transform.scale(frame_surface, new_size)
                
                self.gif_frames.append(frame_surface)
            
            return len(self.gif_frames) > 0
        except Exception as e:
            print(f"Error loading GIF: {e}")
            return False
    
    def get_random_response(self, draw_index, result):
        """Get a random response for the given draw index and result"""
        out = random.choice(self.responses[f"{self.current_draw+1}"][f"{draw_index}/10"])
        return out
        
    def update(self, dt):
        if self.state == "spinning":
            self.wheel.update(dt)
            
            # If wheel stopped spinning
            if not self.wheel.spinning:
                # Record the result
                result, idx = self.wheel.get_selected_segment()
                question_idx, answer = idx.split(".")
                self.results.append(result)
                
                # Select a random response based on the result
                response = self.get_random_response(self.current_draw+1, question_idx)
                self.result_responses.append(response)
                
                # Try to load the corresponding GIF
                if self.load_gif(idx):
                    # Go to showing GIF state
                    self.state = "showing_gif"
                    self.wait_timer = 3.0  # Show GIF for 3 seconds
                else:
                    # If no GIF found, go to waiting state
                    self.state = "waiting"
                    self.wait_timer = 1.5  # Wait 1.5 seconds before next wheel
                
        elif self.state == "showing_gif":
            # Update GIF animation
            self.frame_timer += dt
            if self.frame_timer >= self.frame_delay and self.gif_frames:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            
            # Countdown the wait timer
            self.wait_timer -= dt
            if self.wait_timer <= 0:
                self.current_draw += 1
                
                # Check if we've completed all draws
                if self.current_draw >= self.total_draws:
                    self.state = "results"
                else:
                    # Generate a new wheel and start spinning
                    self.generate_new_wheel()
                    self.wheel.spin()
                    self.state = "spinning"  # Wait for user to spin
                
        elif self.state == "waiting":
            self.wait_timer -= dt
            if self.wait_timer <= 0:
                self.current_draw += 1
                
                # Check if we've completed all draws
                if self.current_draw >= self.total_draws:
                    self.state = "results"
                else:
                    # Generate a new wheel and start spinning
                    self.generate_new_wheel()
                    self.state = "spinning"  # Wait for user to spin
    
    def draw(self, surface):
        # Clear the screen
        surface.fill(tuple(self.config["bg_color"]))
        try:
            if self.config["bg_img"] != "None":
                img = pygame.image.load(os.path.join('assets','backgrounds', self.config["bg_img"]))
                surface.fill((128,128,128))
                surface.blit(img,(0,0),None, pygame.BLEND_RGB_ADD)
        except:
            pass
        
        if self.state == "spinning" or self.state == "waiting":
            # Draw the wheel
            self.wheel.draw(surface)
            
            # Draw progress
            progress_text = self.font.render(f"{QUESTIONS[self.current_draw]}", True, (0, 0, 0))
            self.screen.blit(progress_text, (20, 20))
            
            # Draw current result if waiting
            if self.state == "waiting":
                result = self.results[-1]
                result_text = self.font.render(f"Result: {result}", True, (0, 0, 0))
                self.screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT - 100))
            
            # Draw controls
            if self.state == "spinning" and not self.wheel.spinning:
                instructions = self.font.render("Press SPACE or click to spin", True, (0, 0, 0))
                self.screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 60))
        
        elif self.state == "showing_gif":
            # Display the current GIF frame
            if self.gif_frames and len(self.gif_frames) > self.current_frame:
                frame = self.gif_frames[self.current_frame]
                # Center the frame on screen
                frame_rect = frame.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                self.screen.blit(frame, frame_rect)
                
            # Show the result text above the GIF
            result = self.results[-1]
            result_text = self.font.render(f"Result: {result}", True, (0, 0, 0))
            self.screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 30))
            
            # Show the response text below the GIF
            response = self.result_responses[-1]
            # Create a semi-transparent background for the text
            text_bg_rect = pygame.Rect(0, HEIGHT - 120, WIDTH, 80)
            s = pygame.Surface((text_bg_rect.width, text_bg_rect.height), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))  # Semi-transparent black
            surface.blit(s, text_bg_rect)
            
            # Render the response text with word wrapping
            max_width = WIDTH - 40  # Leave some margin
            lines = self.wrap_text(response, self.response_font, max_width)
            line_height = self.response_font.get_height()
            
            for i, line in enumerate(lines):
                line_surf = self.response_font.render(line, True, (255, 255, 255))
                y_pos = HEIGHT - 110 + (i * line_height)
                self.screen.blit(line_surf, (WIDTH // 2 - line_surf.get_width() // 2, y_pos))
                
        elif self.state == "results":
            # Draw all results
            title = self.font.render("Final Results", True, (0, 0, 0))
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
            

            # Display all results
            result_y = 100
            for i, (result, response) in enumerate(zip(self.results, self.result_responses)):
                # Display result
                result_text = self.small_font.render(f"Draw {i+1}: {result}", True, (0, 0, 0))
                self.screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, result_y))
                result_y += 20
                
                # Display response
                response_text = self.small_font.render(f'"{response}"', True, (80, 80, 80))
                self.screen.blit(response_text, (WIDTH // 2 - response_text.get_width() // 2, result_y))
                result_y += 40
            
            # Draw restart button
            pygame.draw.rect(surface, (100, 100, 255), (WIDTH//2 - 300, HEIGHT - 100, 200, 50), border_radius=10)
            pygame.draw.rect(surface, (0, 0, 0), (WIDTH//2 - 300, HEIGHT - 100, 200, 50), 2, border_radius=10)
            end_text = self.font.render("Zakończ", True, (0, 0, 0))

            color = (100, 255, 100) if self.isresultsaved else (100, 100, 255)
            pygame.draw.rect(surface, color, (WIDTH//2 , HEIGHT - 100, 250, 50), border_radius=10)
            pygame.draw.rect(surface, (0, 0, 0), (WIDTH//2 , HEIGHT - 100, 250, 50), 2, border_radius=10)
            save_text = self.font.render("Zapisz wynik", True, (0, 0, 0))

            self.screen.blit(end_text, (WIDTH // 2 - end_text.get_width() - 270 // 2, HEIGHT - 90))
            self.screen.blit(save_text, (WIDTH // 2 - save_text.get_width() + 450 // 2, HEIGHT - 90))
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a specified width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            width, _ = font.size(test_line)
            if width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def handle_event(self, event):
        if self.state == "spinning" and not self.wheel.spinning:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                self.wheel.spin()
        
        elif self.state == "results":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if restart button was clicked
                mouse_pos = pygame.mouse.get_pos()
                exit_button = pygame.Rect(WIDTH//2 - 300, HEIGHT - 100, 200, 50)
                save_button = pygame.Rect(WIDTH//2 , HEIGHT - 100, 250, 50)
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif save_button.collidepoint(mouse_pos):
                    pygame.image.save(self.screen, "result.png")
                    self.isresultsaved = True