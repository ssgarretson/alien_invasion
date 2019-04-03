import pygame
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from time import sleep

from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
    # Initialize pygame, settings, and screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard 
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    stars = Group()
    asteroids = Group()

    # Create a Starfield for the Background
    gf.create_starfield(ai_settings, screen, stars)

    # Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create an Asteroid field
    gf.create_asteroidfield(ai_settings, screen, asteroids)

# Start the main loop for the game
    while True:
        
        gf.check_events(ai_settings, screen, stats, sb, play_button,
                        ship, aliens, bullets, stars)
       
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids)
            gf.update_stars(ai_settings, screen, stars)
            if stats.level % 10 != 0:
                gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)  
            elif stats.level % 10 == 0:  
                gf.update_asteroids(ai_settings, screen, stats, sb, ship, asteroids, aliens)
       
        gf.update_screen(ai_settings, screen, stats, sb, 
                ship, aliens, bullets, play_button, stars, asteroids)
        
run_game()