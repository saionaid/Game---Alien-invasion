import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien




def check_keydown_events(event, fixtheworld_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #Create a bullet and add it to the bullets group.
        new_bullet = Bullet(fixtheworld_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """Resond to keyup release."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(fixtheworld_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to key presses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, fixtheworld_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(fixtheworld_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(fixtheworld_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """ Stars a new game when the play button is clicked."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:

        # Reset the game settings
        fixtheworld_settings.initialize_dynamic_settings()

        # Hide mouse
        pygame.mouse.set_visible(False)

         # Reset the game stats
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

    # Empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship
    create_fleet(fixtheworld_settings, screen, ship, aliens)
    ship.center_ship()

def update_screen(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # Redraw the screen during each pass through the loop.
    screen.fill(fixtheworld_settings.bg_color)

    #Redraw all bullets behing the ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score info.
    sb.show_score()

    # Draw the play button if game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # makes the most recently drawn screen visible
    pygame.display.flip()

def update_bullets(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and remove old ones."""

    bullets.update()

    # Removing bullets that have gone offscreen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    for aliens in collisions.values():
        stats.score += fixtheworld_settings.alien_points * len(aliens)
        sb.prep_score()
    check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the alien fleet is destroyed then moves up one level.
        bullets.empty()
        fixtheworld_settings.increase_speed()

        # Increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(fixtheworld_settings, screen, ship, aliens)

def create_fleet(fixtheworld_settings, screen, ship, aliens):
    """ Create a fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(fixtheworld_settings, screen)
    number_aliens_x = get_number_aliens_x(fixtheworld_settings, alien.rect.width)
    number_rows = get_number_rows(fixtheworld_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens
    for row_number in range(number_rows):
         for alien_number in range(number_aliens_x):
            creat_alien(fixtheworld_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(fixtheworld_settings, alien_width):
    """ How many aliens will fir in a row."""
    available_space_x = fixtheworld_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (1 * alien_width))
    return number_aliens_x

def creat_alien(fixtheworld_settings, screen, aliens, alien_number, row_number):
    """ Create an alien and place it in a row."""
    alien = Alien(fixtheworld_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 1 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(fixtheworld_settings, ship_height, alien_height):
    """ Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (fixtheworld_settings.screen_height - ( 1* alien_height) - ship_height)
    number_rows = int(available_space_y / ( 2 * alien_height))
    return number_rows

def check_fleet_edges(fixtheworld_settings, aliens):
    """ Respond if any aliens have reched the edge of the screen."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(fixtheworld_settings, aliens)
            break

def change_fleet_direction(fixtheworld_settings, aliens):
    """ Drop the fleet and change the fleets direciton."""
    for alien in aliens.sprites():
        alien.rect.y += fixtheworld_settings.fleet_drop_speed
    fixtheworld_settings.fleet_direction *= -1

def ship_hit(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets):
    """ Respond to a ship being hit by an alien."""
    if stats.ships_left > 0:

        # Decrement Lives left
        stats.ships_left -= 1

        # Update scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(fixtheworld_settings, screen, ship, aliens)
        ship.center_ship()

        #Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets):
    """ Check if aliens have reached the bottom of the screen. """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
           if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets):
    """ Check if the fleet has reached the edge and then update the position of all aliens."""
    check_fleet_edges(fixtheworld_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen
    check_aliens_bottom(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    """ Check to see if there is a new high score. """
    if stats.score > stats.high_score:
            stats.high_score = stats.score
            sb.prep_high_score()


