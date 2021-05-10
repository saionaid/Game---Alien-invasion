import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ Bullets"""
    def __init__(self, fixtheworld_settings, screen, ship):
            """Create a bullet object at the ships position"""
            super(Bullet, self).__init__()
            self.screen = screen

            #Create a bullet rect at position (0,0), then set correct position.
            self.rect = pygame.Rect(0, 0, fixtheworld_settings.bullet_width, fixtheworld_settings.bullet_height)
            self.rect.centerx = ship.rect.centerx
            self.rect.top = ship.rect.top

            # Store the bullet's position as a decimal value.
            self.y = float(self.rect.y)

            self.color = fixtheworld_settings.bullet_color
            self.speed = fixtheworld_settings.bullet_speed

    def update(self):
            """move the bullet up the screen."""
            #update decimal position of the bulllet.
            self.y -= self.speed
            #Update the rect position
            self.rect.y = self.y

    def draw_bullet(self):
            """Draw the bullet on the screen"""
            pygame.draw.rect(self.screen, self.color, self.rect)
