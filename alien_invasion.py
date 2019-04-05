"""Alien Invasion by Sam Garretson"""
import pygame
from time import sleep
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

from settings import Settings
from ship import Ship
import game_functions as gf
import cutscenes as cs

def run_game():
    """Run the game until the user quits"""
    # Initialize pygame, settings, and screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Make the Play button
    play_button = Button(ai_settings, screen, "Play")
    play_button.prep_msg("Play")

    # Create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    stars = Group()
    asteroids = Group()

    # Create an Asteroid field
    gf.create_asteroidfield(ai_settings, screen, asteroids)
    gf.create_starfield(ai_settings, screen, stars)
    


    # Start the main loop for the game
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button,
                        ship, aliens, bullets, stars)
        
        if stats.game_active:
            if stats.play_cutscene:
                cs.opening_cutscene(ai_settings, screen, sb, stars)
                stats.play_cutscene = False
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids)
            if stats.level % ai_settings.asteroid_level != 0:
                gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
            elif stats.level % ai_settings.asteroid_level == 0:
                gf.update_asteroids(ai_settings, screen, stats, sb, ship, asteroids, aliens)

        gf.update_screen(ai_settings, screen, stats, sb,
                         ship, aliens, bullets, play_button, stars, asteroids)
        
        gf.update_stars(ai_settings, stars)


run_game()
