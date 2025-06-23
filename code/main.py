from settings import *
from support import *
from timer import Timer
from monster import *
from random import choice
from ui import *
from attack import AttackAnimationSprite

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Elemental Creatures Battle')
        self.clock = pygame.time.Clock()
        self.running = True
        self.import_assets()
        
        # Stop any existing music before starting new music
        pygame.mixer.stop()  # Stop all current sounds
        if 'music' in self.audio:
            self.audio['music'].stop()  # Stop current music instance
            self.audio['music'].play(-1)  # Start fresh music
        
        self.player_active = True
        # Game state management - tracks game state
        self.game_state = 'selection'  # Can be: 'selection', 'playing', 'win', 'lose'
        
        self.end_game_font = pygame.font.Font(None, 72)     # Large font for win/lose message
        self.instruction_font = pygame.font.Font(None, 36)  # Medium font for instructions        # Initialize creature selection screen
        self.creature_selection = CreatureSelection(self.simple_surfs)
        
        # Game components (will be initialized after creature selection)
        self.all_sprites = None
        self.player_monsters = None
        self.monster = None
        self.opponent = None
        self.opponent_team = None  # List of 5 opponent creatures (increased for difficulty)
        self.current_opponent_index = 0  # Track which opponent creature is active        self.ui = None
        self.opponent_ui = None
        self.timers = None

    def get_input(self, state, data = None):
        if state == 'attack':
            self.apply_attack(self.opponent, data)
        elif state == 'heal':
            # DIFFICULTY: Reduced healing from 50 to 30 to make healing less powerful
            self.monster.health += 30
            AttackAnimationSprite(self.monster, self.attack_frames['green'], self.all_sprites)
            if 'green' in self.audio:
                self.audio['green'].play()
        elif state == 'switch':
            self.monster.kill()
            self.monster = data
            self.all_sprites.add(self.monster)
            self.ui.monster = self.monster

        elif state == 'escape':
            self.running = False
        self.player_active = False
        self.timers['player end'].activate()

    def apply_attack(self, target, attack):
        """
        Apply damage from one Creature to another
        - target: Creature receiving the attack
        - attack: name of the attack being used
        """
        attack_data = ATTACK_DATA[attack]  # Get attack details (damage, element, animation)
        # Calculate type effectiveness multiplier (2x, 1x, or 0.5x damage)
        attack_multiplier = ELEMENT_DATA[attack_data['element']][target.element]
        # Apply damage = base damage × type effectiveness
        target.health -= attack_data['damage'] * attack_multiplier        # Show attack animation on target
        AttackAnimationSprite(target, self.attack_frames[attack_data['animation']], self.all_sprites)
        
        # Play attack sound effect if available
        if attack_data['animation'] in self.audio:
            self.audio[attack_data['animation']].play()

    def opponent_turn(self):
        if self.opponent.health <= 0:
            # Move to next opponent creature
            self.current_opponent_index += 1
            if self.current_opponent_index < len(self.opponent_team):                # Switch to next opponent creature
                self.player_active = True
                self.opponent.kill()
                next_opponent = self.opponent_team[self.current_opponent_index]
                self.opponent = Opponent(next_opponent.name, self.front_surfs[CREATURE_IMAGE_MAP[next_opponent.name]], self.all_sprites)
                self.opponent_ui.monster = self.opponent
                self.opponent_ui.opponent_index = self.current_opponent_index  # Update UI index
            else:
                # Player wins - defeated all opponent creatures
                self.game_state = 'win'
                self.player_active = False
        else:
            # DIFFICULTY: Smarter AI - choose attacks based on type effectiveness
            attack = self.choose_smart_attack()
            self.apply_attack(self.monster, attack)
            self.timers['opponent end'].activate()

    def choose_smart_attack(self):
        """AI chooses attacks more strategically based on type effectiveness and damage"""
        from random import random
        
        # Get player monster's element
        player_element = CREATURE_DATA[self.monster.name]['element']
        
        # Categorize attacks by effectiveness and damage
        super_effective_attacks = []
        high_damage_attacks = []
        normal_attacks = []
        
        for attack_name in self.opponent.abilities:
            attack_element = ATTACK_DATA[attack_name]['element']
            attack_damage = ATTACK_DATA[attack_name]['damage']
            
            # Check type effectiveness
            effectiveness = 1.0
            if attack_element in ELEMENT_DATA:
                effectiveness = ELEMENT_DATA[attack_element].get(player_element, 1.0)
            
            # Categorize attack
            if effectiveness > 1.0:  # Super effective
                super_effective_attacks.append(attack_name)
            elif attack_damage >= 40:  # High damage attacks
                high_damage_attacks.append(attack_name)
            else:
                normal_attacks.append(attack_name)
        
        # DIFFICULTY: Smarter attack selection
        # 60% chance for super effective, 30% for high damage, 10% for normal
        rand = random()
        if super_effective_attacks and rand < 0.6:
            return choice(super_effective_attacks)
        elif high_damage_attacks and rand < 0.9:
            return choice(high_damage_attacks)
        elif normal_attacks:
            return choice(normal_attacks)
        else:
            # Fallback to any attack
            return choice(self.opponent.abilities)

    def player_turn(self):
        self.player_active = True
        if self.monster.health <= 0:
            available_monsters = [monster for monster in self.player_monsters if monster.health > 0]
            if available_monsters:
                self.monster.kill()
                self.monster = available_monsters[0]
                self.all_sprites.add(self.monster)
                self.ui.monster = self.monster
            else:
                # Player loses - all monsters defeated
                self.game_state = 'lose'
                self.player_active = False

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def restart_game(self):
        """Properly restart the game by stopping all audio and going back to creature selection"""
        # Stop all sound effects and music
        pygame.mixer.stop()
        if hasattr(pygame.mixer.music, 'stop'):
            pygame.mixer.music.stop()
          # Clear all sprites if they exist
        if self.all_sprites:
            self.all_sprites.empty()
        
        # Reset to creature selection state
        self.game_state = 'selection'
        self.player_active = True
        
        # Reinitialize audio
        self.import_assets()
        if 'music' in self.audio:
            self.audio['music'].play(-1)
        
        # Reset creature selection
        self.creature_selection = CreatureSelection(self.simple_surfs)
        
        # Clear game components (will be recreated after selection)
        self.all_sprites = None
        self.player_monsters = None
        self.monster = None
        self.opponent = None
        self.opponent_team = None
        self.current_opponent_index = 0
        self.ui = None
        self.opponent_ui = None
        self.timers = None

    def handle_end_game_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Stop all audio before restarting
                    pygame.mixer.stop()  # Stop all sound effects
                    pygame.mixer.music.stop()  # Stop background music
                    # Restart the game
                    self.restart_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw_end_game_screen(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))
        
        # Win/Lose message
        if self.game_state == 'win':
            main_text = "YOU WIN!"
            main_color = (0, 255, 0)  # Green
        else:
            main_text = "YOU LOSE!"
            main_color = (255, 0, 0)  # Red
            
        main_surf = self.end_game_font.render(main_text, True, main_color)
        main_rect = main_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        self.display_surface.blit(main_surf, main_rect)
          # Instructions with better visibility
        restart_text = "🎮 Press SPACEBAR to Play Again 🎮"
        restart_surf = self.instruction_font.render(restart_text, True, (255, 255, 100))  # Yellow for better visibility
        restart_rect = restart_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
        self.display_surface.blit(restart_surf, restart_rect)
        
        exit_text = "Press ESC to Exit"
        exit_surf = self.instruction_font.render(exit_text, True, (200, 200, 200))
        exit_rect = exit_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 60))
        self.display_surface.blit(exit_surf, exit_rect)

    def import_assets(self):
        self.back_surfs = folder_importer('images', 'back')
        self.front_surfs = folder_importer('images', 'front')
        self.bg_surfs = folder_importer('images', 'other')
        self.simple_surfs = folder_importer('images', 'simple')
        self.attack_frames = tile_importer(4,'images', 'attacks')
        self.audio = audio_importer('audio')

    def draw_monster_floor(self):
        if self.all_sprites is not None:
            for sprite in self.all_sprites:
                if isinstance(sprite, Creature):
                    floor_rect = self.bg_surfs['floor'].get_rect(center = sprite.rect.midbottom + pygame.Vector2(0, -10))
                    self.display_surface.blit(self.bg_surfs['floor'], floor_rect)

    def display_end_game_message(self, message):
        text_surface = self.end_game_font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.display_surface.blit(text_surface, text_rect)

        instruction_surface = self.instruction_font.render("Press 'R' to restart or 'Q' to quit", True, (255, 255, 255))
        instruction_rect = instruction_surface.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.display_surface.blit(instruction_surface, instruction_rect)

    def initialize_battle(self, selected_creatures):
        """Initialize the battle after creature selection is complete"""
        # Sprite groups - containers that hold and manage game objects
        self.all_sprites = pygame.sprite.Group()  # Holds all visible game sprites
        
        # Create creature objects using the selected creatures
        self.player_monsters = [Monster(name, self.back_surfs[CREATURE_IMAGE_MAP[name]]) for name in selected_creatures]
        self.monster = self.player_monsters[0]  # Currently active creature (first in list)
        self.all_sprites.add(self.monster)      # Add active creature to sprite group for rendering
          # Create opponent team - 5 random creatures (excluding player's creatures to avoid duplicates)
        # DIFFICULTY: Increased from 4 to 5 opponents to make game longer and harder
        available_opponents = [name for name in CREATURE_DATA.keys() if name not in selected_creatures]
        if len(available_opponents) < 5:
            # If not enough unique creatures, allow duplicates
            available_opponents = list(CREATURE_DATA.keys())
        
        self.opponent_team = []
        for i in range(5):
            opponent_name = choice(available_opponents)
            opponent_monster = Monster(opponent_name, self.front_surfs[CREATURE_IMAGE_MAP[opponent_name]])
            self.opponent_team.append(opponent_monster)
            # Remove from available to avoid immediate duplicates (but could repeat if needed)
            if opponent_name in available_opponents:
                available_opponents.remove(opponent_name)
            if not available_opponents:  # If we run out, refill
                available_opponents = [name for name in CREATURE_DATA.keys()]
        
        # Set first opponent as active
        self.opponent = Opponent(self.opponent_team[0].name, self.front_surfs[CREATURE_IMAGE_MAP[self.opponent_team[0].name]], self.all_sprites)
        self.current_opponent_index = 0
        
        # ui
        self.ui = UI(self.monster, self.player_monsters, self.simple_surfs, self.get_input)
        self.opponent_ui = OpponentUI(self.opponent, self.current_opponent_index, len(self.opponent_team))# timers
        self.timers = {'player end': Timer(1000, func = self.opponent_turn), 'opponent end': Timer(1000, func = self.player_turn)}
        
        # Set player as active and change to playing state
        self.player_active = True
        self.game_state = 'playing'

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            
            if self.game_state == 'selection':                # Creature selection events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                
                # Handle creature selection
                if self.creature_selection.handle_input():
                    # Selection complete, initialize battle
                    self.initialize_battle(self.creature_selection.selected_creatures)
                
                # Draw creature selection screen
                self.creature_selection.draw()
                
            elif self.game_state == 'playing':
                # Normal game events
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.running = False
               
                # update
                self.update_timers()
                self.all_sprites.update(dt)
                if self.player_active:
                    self.ui.update()                # draw  
                self.display_surface.blit(self.bg_surfs['bg'], (0,0))
                self.draw_monster_floor()
                self.all_sprites.draw(self.display_surface)
                self.ui.draw()
                self.opponent_ui.draw()
                
            elif self.game_state in ['win', 'lose']:
                # Handle end game input
                self.handle_end_game_input()
                
                # Continue drawing the game background
                self.display_surface.blit(self.bg_surfs['bg'], (0,0))
                self.draw_monster_floor()
                if self.all_sprites is not None:
                    self.all_sprites.draw(self.display_surface)
                if self.ui is not None:
                    self.ui.draw()
                if self.opponent_ui is not None:
                    self.opponent_ui.draw()
                
                # Draw end game screen overlay
                self.draw_end_game_screen()
            
            pygame.display.update()
        
        pygame.quit()
    
if __name__ == '__main__':
    game = Game()
    game.run()