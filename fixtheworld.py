import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_funtions as gf



def run_game():
    """Initiates the game and creates a screen object."""
    pygame.init()
    fixtheworld_settings = Settings()
    screen = pygame.display.set_mode((fixtheworld_settings.screen_width, fixtheworld_settings.screen_height))
    pygame.display.set_caption("fixtheworld")

    # Make a play button
    play_button = Button(fixtheworld_settings, screen, "Play!")

    # Create an instance to store game stats and create a scoreboard
    stats = GameStats(fixtheworld_settings)
    sb = Scoreboard(fixtheworld_settings, screen, stats)

    # Make a ship, a group of bullets and a group of aliens.
    ship = Ship(fixtheworld_settings, screen)
    bullets = Group()
    aliens = Group()

    # Create a fleet of aliens
    gf.create_fleet(fixtheworld_settings, screen, ship, aliens)

    # Starts the main loop for the game.
    while True:
        gf.check_events(fixtheworld_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(fixtheworld_settings, screen, stats, sb, ship, aliens, bullets, play_button)



run_game()