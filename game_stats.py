class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Start Alien Invasion in an inactive state
        self.game_active = False

        # High score should never be reset
        f = open("highscore.txt", "r")
        self.high_score = int(f.read())
        f.close()
    
    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        self.asteroids_dodged = 0