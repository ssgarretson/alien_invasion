import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship1.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement Flag
        self.moving_right = False
        self.moving_left = False
    
    def center_ship(self):
        """Center the ship on the screen"""
        self.center = self.screen_rect.centerx
    
    def update(self):
        """Update the ship's position based on the movement flag"""

        # Update the ship's center value, not the rect
        if self.moving_left and self.rect.left > 0:
            self.image = pygame.image.load('images/ship3.bmp')
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.image = pygame.image.load('images/ship2.bmp')
            self.center += self.ai_settings.ship_speed_factor
        elif not self.moving_left and not self.moving_right:
            self.image = pygame.image.load('images/ship1.bmp')

        # Update rect object from self.center
        self.rect.centerx = self.center

        # Initialize the ships sounds
        self.hit_sound = pygame.mixer.Sound("sounds/hit.wav")
        self.asteroids_sound = pygame.mixer.Sound("sounds/asteroids.wav")
 
    
    def update_ship_image(self, image):
        self.image = pygame.image.load('images/{}.bmp'.format(image))

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def hit(self):
        """Make a hit sound when the ship is hit"""
        pygame.mixer.Sound.play(self.hit_sound)