import pygame
from pygame.sprite import Sprite

class Ship(Sprite):


    def __init__(self, fixtheworld_settings, screen):
            """Initialize our ship and set its starting position"""
            super(Ship, self).__init__()
            self.screen = screen
            self.fixtheworld_settings = fixtheworld_settings
            # Load ship image
            self.image = pygame.image.load('images/ship.bmp')
            self.rect = self.image.get_rect()
            self.screen_rect = screen.get_rect()

            #Starts each new ship at the bottom center of the screen

            self.rect.centerx = self.screen_rect.centerx
            self.rect.bottom = self.screen_rect.bottom

            #Storing a Float for the ships center

            self.center = float(self.rect.centerx)

            # Movement flag
            self.moving_right = False
            self.moving_left = False
    def update(self):
            """Updates ships position based on the movement flag."""
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.fixtheworld_settings.ship_speed
            if self.moving_left and self.rect.left > 0:
                self.center -= self.fixtheworld_settings.ship_speed
            # Update rect object from self.center
            self.rect.centerx = self.center


    def blitme(self):
            """Draw the ship at its current location."""
            self.screen.blit(self.image, self.rect)

    def center_ship(self):
            """ Center the ship on the screen. """
            self.center = self.screen_rect.centerx