import sys
from time import sleep
from random import randint

import pygame

from bullet import Bullet
from alien import Alien
from star import Star
from asteroid import Asteroid

def check_events(ai_settings, screen, stats, sb, play_button, 
                 ship, aliens, bullets, stars):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
                    aliens, bullets, stars, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
                      aliens, bullets, stars, mouse_x, mouse_y):
    """Start a new game when the player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        stars.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        create_starfield(ai_settings, screen, stars)
        ship.center_ship()

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT and stats.game_active:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT and stats.game_active:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and stats.game_active:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sb.update_highscore()
        sys.exit()
    
def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, stars, asteroids):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)

    # Draw a starfield
    for star in stars:
        star.blitme()

    # Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    
    if stats.level % ai_settings.asteroid_level != 0:
        aliens.draw(screen)
    else:
        asteroids.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible
    pygame.display.flip()

def fire_bullets(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet"""
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids):
    """Update the position of bullets and get rid of old bulelts"""
    # Update bullet positions
    bullets.update() 

     # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids):
    """Respond to bullet-alien collisions"""
    
    # Check for any bullets that have hit aliens
    # If so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)


    if len(aliens) == 0 and stats.level % ai_settings.asteroid_level != 0:
        # If the entire fleet is destroyed, start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

        if stats.level % ai_settings.asteroid_level != 0:
            create_fleet(ai_settings, screen, ship, aliens)
        else:
            create_asteroidfield(ai_settings, screen, asteroids)

def check_asteroid_ship_collisions(stats, sb, ship, asteroids):
    """Respond to asteroid-ship collisions"""
    # Check for any asteroids that have hit the ship
    # If so, player loses a life
    if pygame.sprite.spritecollide(ship, asteroids, True):
        if stats.ships_left > 0:
            # Decrement ships_left
            stats.ships_left -= 1

            # Update Scoreboard
            sb.prep_ships()
        else:
            stats.game_active = False
            pygame.mouse.set_visible(True)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height - 
                        (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height)) - 1
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x 
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Create an alien and find the number of aliens in a row
    # Spacing between each alien is equal to one alien width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
        alien.rect.height)
    

    # Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, 
                alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    if stats.ships_left > 0:
        # Decrement ships_left
        stats.ships_left -= 1

        # Update Scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check if the fleet is at an edge,
        and then Update the positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Loof for aliens hittinf the bottom of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    """Check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.score_text_color = (255, 204, 0)
        sb.prep_score()
        sb.prep_high_score()

def create_starfield(ai_settings, screen, stars):
    """Create a field of stars"""
    for star_number in range(0, ai_settings.star_number):
        star = create_star(ai_settings, screen)
        stars.add(star)
        star_number += 1

def create_star(ai_settings, screen):
    """Create a single star"""
    star = Star(ai_settings, screen)
    star.rect.x = randint(-5, 1223)
    star.rect.y = randint(-5, 805)
    return star

def update_stars(ai_settings, stars):
    """Update the position of stars and get rid of old stars"""
    # Update star positions
    stars.update()

    # Replace Disappeaing Stars
    for star in stars.copy():
        if star.rect.y >= ai_settings.screen_height:
            star.rect.y = randint(-20, -5)
            star.rect.x = randint(-5, 1223)

def create_asteroidfield(ai_settings, screen, asteroids):
    """Create a field of asteroids"""
    for asteroid_number in range(0, ai_settings.asteroid_number):
        asteroid = create_asteroid(ai_settings, screen)
        asteroids.add(asteroid)
        asteroid_number += 1
    
def create_asteroid(ai_settings, screen):
    """Create a single Asteroid"""
    asteroid = Asteroid(ai_settings, screen)
    asteroid.rect.x = randint(-5, 1223)
    asteroid.rect.y = randint(-1000, -10)
    return asteroid

def update_asteroids(ai_settings, screen, stats, sb, ship, asteroids, aliens):
    """Update the position of asteroids and get rid of old Asteroids"""
    # Update asteroid positions
    asteroids.update()

    for asteroid in asteroids.copy():
        if asteroid.rect.bottom >= ai_settings.screen_height:
            asteroids.remove(asteroid)
            asteroids.add(create_asteroid(ai_settings, screen))
            stats.asteroids_dodged += 1

            # When the player has dodged 500 asteroids they pass the level
            if stats.asteroids_dodged >= 50:
                asteroids.empty()
                stats.level += 1
                sb.prep_level()
                stats.asteroids_dodged = 0
                create_fleet(ai_settings, screen, ship, aliens)
    
    # Check for asteroid-ship collisions
    check_asteroid_ship_collisions(stats, sb, ship, asteroids)

    
    
    