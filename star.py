import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    """A class to represent a sing star in a starfield"""

    def __init__(self, ai_settings, screen):
        """Initialize the star and set its starting position"""
        super(Star, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the star image and get its rect attribute
        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()
       
        # Start each new star near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the bullet's x, y positions as decimal values
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.speed_factor = ai_settings.star_speed_factor

    def update(self):
        """Move the stars slowly down the Screen"""
        # Update the decimal position of the star
        self.rect.y += 5

    def blitme(self):
        """Draw the star at its current location"""
        self.screen.blit(self.image, self.rect)