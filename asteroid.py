import pygame
from pygame.sprite import Sprite

class Asteroid(Sprite):
    """A class to represent a single asteroid in a field"""

    def __init__(self, ai_settings, screen):
        """Initialize the asteroid and set its starting position"""
        super(Asteroid, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/asteroid.bmp')
        self.rect = self.image.get_rect()
    
        # Start each new asteroid near the top left of the screen
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height 

        self.speed_factor = ai_settings.asteroid_speed_factor

    def blitme(self):
        """Draw the asteroid at its current position"""
        self.screen.blit(self.image, self.rect)
        
    def update(self):
        """Move the asteroid down right or left"""
        self.rect.y += self.speed_factor
        pygame.transform.rotate(self.image, 10)