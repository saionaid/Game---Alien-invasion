



class GameStats():
    """ Track stats for game. """
    def __init__(self, fixtheworld_settings):
        """ Initialize stats. """
        self.fixtheworld_settings = fixtheworld_settings
        self.reset_stats()

        # Start Game in an active state.
        self.game_active = False

        # High Score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """  Initialize stats that can gance during the game. """
        self.ships_left = self.fixtheworld_settings.ship_limit
        self.score = 0
        self.level = 1

