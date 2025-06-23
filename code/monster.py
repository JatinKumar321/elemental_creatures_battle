from settings import * 
from random import sample

class Creature:
    """
    Base class for all creatures in the game
    Handles basic stats like health, element type, and available attacks
    """
    def get_data(self, name):
        """
        Load creature data from settings file
        - name: Creature name (like 'Sparkfin', 'Emberclaw', etc.)
        """
        # Get element type (flame, aqua, nature) and health from creature database
        self.element = CREATURE_DATA[name]['element']
        self._health = self.max_health = CREATURE_DATA[name]['health']
        # Randomly choose 4 attacks from all available attacks for this creature
        self.abilities = sample(list(ATTACK_DATA.keys()), 4)
        self.name = name  # Store creature's name
    
    @property
    def health(self):
        """Get current health points"""
        return self._health
    
    @health.setter
    def health(self, value):
        """
        Set health with bounds checking
        Health cannot go below 0 or above max_health
        """
        self._health = min(self.max_health, max(0, value))

class Monster(pygame.sprite.Sprite, Creature):
    """
    Player's creature - appears on the left side of screen
    This represents the creature you control in battle
    """
    def __init__(self, name, surf):
        super().__init__()  # Initialize sprite functionality
        self.image = surf   # Creature sprite image (back view)
        # Position creature on left side of screen, at bottom
        self.rect = self.image.get_rect(bottomleft = (100, WINDOW_HEIGHT))
        self.get_data(name)  # Load creature stats and attacks
    
    def __repr__(self):
        """String representation showing name and health status"""
        return f'{self.name}: {self.health}/{self.max_health}'

class Opponent(pygame.sprite.Sprite, Creature):
    """
    Enemy creature - appears on the right side of screen
    This is the creature you're fighting against
    """
    def __init__(self, name, surf, groups):
        super().__init__(groups)  # Initialize sprite and add to sprite groups
        self.image = surf         # Creature sprite image (front view)
        # Position creature on right side of screen
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH - 250, 300))
        self.get_data(name)       # Load creature stats and attacks