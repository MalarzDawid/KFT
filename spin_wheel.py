import pygame
import sys
import math
import random
from pygame import gfxdraw
import time
from constants import CENTER, WHEEL_RADIUS, SEGMENT_COLORS, FONT_SIZE
import pygame.mixer

pygame.mixer.init()
SPIN_SOUND = pygame.mixer.Sound("sample.mp3")


class SpinWheel:
    def __init__(self, segments):
        self.segments = segments
        self.segment_count = len(self.segments)
        self.segment_angle = 360 / self.segment_count
        self.angle = 0  # Current rotation angle
        self.target_angle = 0  # Target angle after spinning
        self.angular_velocity = 2  # Current speed
        self.deceleration = 0  # Deceleration rate when stopping
        self.spinning = False
        self.indicator_point = (CENTER[0], CENTER[1] - WHEEL_RADIUS - 20)
        self.spin_sound = SPIN_SOUND
    
    def spin(self):
        if not self.spinning:
            self.spinning = True
            self.spin_sound.play(-1)
            # Random initial velocity between 720 and 1080 degrees per second
            # Negative value for clockwise rotation
            self.angular_velocity = -1080
            # Random additional rotation between 2 and 10 full rotations
            additional_rotation = random.uniform(6.8, 6.8) * 360
            self.target_angle = self.angle - additional_rotation  # Subtract for clockwise
            # Calculate deceleration to stop at target_angle
            # Using the formula: v²/2a = distance
            # We solve for a (deceleration)
            self.deceleration = (self.angular_velocity ** 2) / (2 * -additional_rotation)
    
    def update(self, dt):
        if self.spinning:
            # Update angle based on current velocity and time
            self.angle += self.angular_velocity * dt
            
            # Increase velocity based on deceleration (velocity is negative)
            self.angular_velocity -= self.deceleration * dt
            
            # Check if we should stop spinning (velocity becomes positive)
            if self.angular_velocity >= 0:
                self.angular_velocity = 0
                self.spinning = False
                # Ensure we stop exactly at the target angle
                self.angle = self.target_angle
                self.spin_sound.stop()
        
        # Keep angle normalized
        self.angle %= 360
    
    def draw(self, surface):
        # Draw wheel segments
        for i in range(self.segment_count):
            start_angle = math.radians(self.angle + i * self.segment_angle)
            end_angle = math.radians(self.angle + (i + 1) * self.segment_angle)
            
            # Get points for the segment
            points = [CENTER]
            for angle in [start_angle, end_angle]:
                x = CENTER[0] + WHEEL_RADIUS * math.cos(angle)
                y = CENTER[1] - WHEEL_RADIUS * math.sin(angle)
                points.append((int(x), int(y)))
            
            # Draw segment
            color = SEGMENT_COLORS[i % len(SEGMENT_COLORS)]
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, (0, 0, 0), points, 2)  # Border
            
            # Draw segment text (without rotation)
            mid_angle = (start_angle + end_angle) / 2
            # Use a smaller radius for text to ensure it stays inside the segment
            text_radius = WHEEL_RADIUS * 0.65
            text_x = CENTER[0] + text_radius * math.cos(mid_angle)
            text_y = CENTER[1] - text_radius * math.sin(mid_angle)
            
            # Use a smaller font for narrow segments
            if self.segment_count > 6:
                text_font = pygame.font.SysFont("Arial", FONT_SIZE - 4, bold=True)
            else:
                text_font = pygame.font.SysFont("Arial", FONT_SIZE - 4, bold=True)
                
            # Render segment text
            text_surface = text_font.render(self.segments[i], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            
            surface.blit(text_surface, text_rect)
        
        # Draw center circle
        pygame.draw.circle(surface, (255, 255, 255), CENTER, 20)
        pygame.draw.circle(surface, (0, 0, 0), CENTER, 20, 2)
        
        # Draw indicator triangle
        indicator_points = [
            (self.indicator_point[0], self.indicator_point[1]),
            (self.indicator_point[0] - 15, self.indicator_point[1] - 30),
            (self.indicator_point[0] + 15, self.indicator_point[1] - 30)
        ]
        pygame.draw.polygon(surface, (200, 0, 0), indicator_points)
        pygame.draw.polygon(surface, (0, 0, 0), indicator_points, 2)
    
    def get_selected_segment(self):
        # The indicator is at the top (90 degrees in standard coordinates)
        # For pygame coordinates, that's at 270 degrees (as y is flipped)
        indicator_position = 90
        
        # Calculate the relative position considering wheel rotation
        # We use (360 - angle % 360) to account for the clockwise rotation
        adjusted_angle = (360 - self.angle % 360)
        relative_position = (adjusted_angle + indicator_position) % 360
        
        # Determine which segment this falls into
        segment_index = int(relative_position / self.segment_angle)
        
        idx = random.randint(1, 5)
        return self.segments[segment_index % self.segment_count], f"{(segment_index % self.segment_count) + 1}.{idx}"
    