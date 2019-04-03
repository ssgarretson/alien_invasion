class Settings():
    """A class to store all the settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen Settings
        self.screen_width = 1218
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship Settings
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_width = 3
        self.bullet_height = 20
        self.bullet_color = 255, 50, 50
        self.bullets_allowed = 5

        # Alien Settings
        self.fleet_drop_speed = 20

        # Star Settings
        self.star_number = 25

        # Asteroid Settings
        self.asteroid_number = 12
        self.asteroid_level = 5
 
        # How quickly the gem speeds up
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """Initialize the game's dynamic settings"""
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 15
        self.alien_speed_factor = 5
        self.star_speed_factor = 2
        self.asteroid_speed_factor = 13

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.star_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
