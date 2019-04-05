import sys
import pygame
from pygame.sprite import Group
from time import sleep
from alien import Alien
from asteroid import Asteroid
from button import Button
import game_functions as gf

def opening_cutscene(ai_settings, screen, sb, stars):
    """A function to play the opening cutscence"""
    
    # Set up the aliens
    alien = Alien(ai_settings, screen)
    alien2 = Alien(ai_settings, screen)
    alien2.rect.x = ai_settings.screen_width
    alien2.rect.y = ai_settings.screen_height / 2
    
    # Set up the Flashing Warning
    warning_button = Button(ai_settings, screen, "DANGER AHEAD!!!")
    warning_button.button_color = (255, 0, 0)
    warning_button.prep_msg("DANGER AHEAD!!!")
    warning_sound = pygame.mixer.Sound("sounds/warning.wav")

    warning = 0
    
    # Set up the asteroids
    asteroids = Group()
    gf.create_asteroidfield(ai_settings, screen, asteroids)
    
    screen.fill(ai_settings.bg_color)

    screen_rect = screen.get_rect()
    
    playing = True
    alien_on_screen = True
    
    pygame.mixer.Sound.play(warning_sound, 1)
    
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sb.update_highscore()
                    sys.exit()
        
        screen.fill(ai_settings.bg_color)
       
        for star in stars:
            star.blitme()
        gf.update_stars(ai_settings, stars)

        # Move the asteroids and the aliens
        if alien_on_screen:
            alien.blitme()
            alien2.blitme()
            for i in range(0, 3):
                alien.update()
                alien2.rect.x -= ai_settings.alien_speed_factor + 5
                i += 1
            if alien.rect.right >= screen_rect.right + alien.rect.width + 20:
                alien_on_screen = False
                del alien, alien2
        for asteroid in asteroids:
            asteroid.blitme()
            asteroid.rect.y += 15
            if asteroid.rect.bottom >= ai_settings.screen_height + 200:
                asteroids.remove(asteroid)

        # Flash the Warning Buttpn
        if warning % 25 < 13:
            warning_button.draw_button()
        warning += 1
        

        # End the scene when the asteroids exit
        if len(asteroids) == 0:
            playing = False

        # Make the most recently drawn screen visible
        pygame.display.flip()



