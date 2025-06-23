import pygame
from os.path import join 
from os import walk

# Game window dimensions (width x height in pixels)
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 

# Creature name to image file mapping
# Since image files have the old monster names, we map new creature names to the correct image files
CREATURE_IMAGE_MAP = {
    # Nature Type Creatures (map to original plant monsters)
    'Verdian': 'Plumette',       # Small green forest spirit
    'Thornwick': 'Ivieron',      # Medium thorny plant beast  
    'Bloomtail': 'Pluma',        # Large flowering creature
    'Podling': 'Pouch',          # Seed-pod creature
    'Dreamleaf': 'Draem',        # Mystical plant being
    'Bugwort': 'Larvea',         # Small insect-plant hybrid
    'Fernblade': 'Cleaf',        # Blade-leafed warrior
    
    # Flame Type Creatures (map to original fire monsters)
    'Sparkfin': 'Sparchu',       # Electric spark creature
    'Emberclaw': 'Cindrill',     # Fire-breathing lizard
    'Blazewing': 'Charmadillo',  # Evolved flame beast
    'Scorchtail': 'Atrox',       # Fiery predator
    'Flamefeather': 'Jacana',    # Fire-bird creature
    
    # Aqua Type Creatures (map to original water monsters)
    'Splashfin': 'Finsta',       # Simple water fish
    'Goldstream': 'Gulfin',      # Golden aquatic creature
    'Starburst': 'Finiette',     # Star-shaped water spirit
    'Mistpuddle': 'Friolera',    # Misty water creature
}

# Color definitions using hex color codes
COLORS = {
    'black': '#000000',   # Pure black
    'red': '#ee1a0f',     # Bright red for damage/danger
    'gray': 'gray',       # Standard gray for UI elements
    'white': '#ffffff',   # Pure white for text/highlights
}

# Creature data - each creature has an element type and health points
# Health determines how much damage they can take before being defeated
# DIFFICULTY: Increased health values to make battles more challenging
CREATURE_DATA = {
    # Nature/Plant Type Creatures (strong vs Aqua, weak vs Flame)
    'Verdian':     {'element': 'nature', 'health': 120},  # Forest spirit starter (+30)
    'Thornwick':   {'element': 'nature', 'health': 180},  # Evolved thorny beast (+40)
    'Bloomtail':   {'element': 'nature', 'health': 200},  # Final flower form (+40)
    'Podling':     {'element': 'nature', 'health': 100},  # Seed creature (+20)    'Dreamleaf':   {'element': 'nature', 'health': 140},  # Mystical plant (+30)
    'Bugwort':     {'element': 'nature', 'health': 65},   # Bug-plant hybrid (+25)
    'Fernblade':   {'element': 'nature', 'health': 115},  # Blade-leafed warrior (+25)
    
    # Flame Type Creatures (strong vs Nature, weak vs Aqua)
    'Sparkfin':    {'element': 'flame', 'health': 95},    # Electric spark creature (+25)
    'Emberclaw':   {'element': 'flame', 'health': 130},   # Fire-breathing lizard (+30)
    'Blazewing':   {'element': 'flame', 'health': 155},   # Evolved flame beast (+35)
    'Scorchtail':  {'element': 'flame', 'health': 75},    # Fiery predator (+25)
    'Flamefeather': {'element': 'flame', 'health': 85},   # Fire-bird creature (+25)
    
    # Aqua Type Creatures (strong vs Flame, weak vs Nature)
    'Splashfin':   {'element': 'aqua', 'health': 75},     # Simple water fish (+25)
    'Goldstream':  {'element': 'aqua', 'health': 105},    # Golden aquatic creature (+25)
    'Starburst':   {'element': 'aqua', 'health': 130},    # Star-shaped water spirit (+30)
    'Mistpuddle':  {'element': 'aqua', 'health': 95},     # Misty water creature (+25)
}

# Creature abilities/attacks - each has damage, element type, and visual animation
# Damage: how much health the attack removes from opponent
# Element: determines effectiveness against different creature types
# Animation: which visual effect to show when attack is used
ATTACK_DATA = {
    # Normal type attacks (neutral damage vs all types)
    'claw_strike':  {'damage': 20, 'element': 'normal', 'animation': 'scratch'},    # Basic physical attack
    'body_slam':    {'damage': 25, 'element': 'normal', 'animation': 'scratch'},    # Body slam attack
    
    # Flame type attacks (super effective vs Nature, not very effective vs Aqua)
    'fire_blast':   {'damage': 35, 'element': 'flame',  'animation': 'fire'},       # Small flames
    'inferno':      {'damage': 50, 'element': 'flame',  'animation': 'explosion'},  # Big fire blast
    
    # Aqua type attacks (super effective vs Flame, not very effective vs Nature)  
    'water_blast':  {'damage': 30, 'element': 'aqua',   'animation': 'splash'},     # Water blast
    'frost_beam':   {'damage': 50, 'element': 'aqua',   'animation': 'ice'},        # Freezing beam
    
    # Nature type attacks (super effective vs Aqua, not very effective vs Flame)
    'thorn_whip':   {'damage': 40, 'element': 'nature', 'animation': 'green'},      # Thorny vine attack
    'leaf_storm':   {'damage': 45, 'element': 'nature', 'animation': 'green'},      # Sharp leaf projectiles
}

# Type effectiveness chart - determines damage multipliers
# 2.0 = super effective (double damage)
# 0.5 = not very effective (half damage)  
# 1.0 = normal effectiveness
ELEMENT_DATA = {
    'flame':  {'aqua': 0.5, 'nature': 2.0, 'flame': 1.0, 'normal': 1.0},   # Flame burns Nature, Aqua extinguishes Flame
    'aqua':   {'aqua': 1.0, 'nature': 0.5, 'flame': 2.0, 'normal': 1.0},   # Aqua puts out Flame, Nature absorbs Aqua
    'nature': {'aqua': 2.0, 'nature': 1.0, 'flame': 0.5, 'normal': 1.0},   # Nature drinks Aqua, Flame burns Nature
    'normal': {'aqua': 1.0, 'nature': 1.0, 'flame': 1.0, 'normal': 1.0},   # Normal type has no advantages/disadvantages
}