class Settings():
    """ PLace to store our game settings"""

    def __init__(self):
        """ Screen settings"""
        self.screen_width = 1600
        self.screen_height = 800
        self.bg_color = (135, 206, 250)

        # Ship settings

        self.ship_limit = 3

        # Bullet Settings

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60

        # Alien settings

        self.fleet_drop_speed = 3

        # How guickly game speeds up
        self.speedup_scale = 1.3

        # How quilckly the alien point values increase.
        self.score_scale = 15

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Initialize settings that change during the game. """
        self.ship_speed = 4.5
        self.bullet_speed = 6
        self.alien_speed_factor = 1

        # Fleet direction of 1 represents rigth; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """ Increase speed settings and alien point values. """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)



