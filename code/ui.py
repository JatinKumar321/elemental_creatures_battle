from settings import *
import math 

class UI:
    def __init__(self, monster, player_monsters, simple_surfs, get_input):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 28)
        self.large_font = pygame.font.Font(None, 36)
        self.left = WINDOW_WIDTH / 2 - 120 
        self.top = WINDOW_HEIGHT / 2 + 60
        self.monster = monster
        self.simple_surfs = simple_surfs
        self.get_input_callback = get_input

        # control 
        self.general_options = ['⚔️ Attack', '💚 Heal', '🔄 Switch', '🚪 Escape']
        self.general_index = {'col': 0, 'row': 0}
        self.attack_index = {'col': 0, 'row': 0}
        self.state = 'general'
        self.rows, self.cols = 2,2
        self.visible_monsters = 4
        self.player_monsters = player_monsters
        self.available_monsters = [monster for monster in self.player_monsters if monster != self.monster and monster.health > 0]
        self.switch_index = 0
        
        # Animation variables
        self.pulse_timer = 0
        self.hover_scale = 1.0
        
        # Element colors for visual feedback
        self.element_colors = {
            'flame': (255, 120, 120),
            'aqua': (120, 180, 255), 
            'nature': (120, 255, 120),
            'normal': (200, 200, 200)
        }
        
        # Key tracking for compatibility
        self.previous_keys = pygame.key.get_pressed()
        self.current_keys = pygame.key.get_pressed()

    def input(self):
        # Update key states for manual just_pressed detection
        self.previous_keys = self.current_keys
        self.current_keys = pygame.key.get_pressed()
        
        # Manual just_pressed implementation
        def just_pressed(key):
            return self.current_keys[key] and not self.previous_keys[key]
        
        if self.state == 'general':
            if just_pressed(pygame.K_DOWN):
                self.general_index['row'] = (self.general_index['row'] + 1) % self.rows
            if just_pressed(pygame.K_UP):
                self.general_index['row'] = (self.general_index['row'] - 1) % self.rows
            if just_pressed(pygame.K_RIGHT):
                self.general_index['col'] = (self.general_index['col'] + 1) % self.cols
            if just_pressed(pygame.K_LEFT):
                self.general_index['col'] = (self.general_index['col'] - 1) % self.cols
            if just_pressed(pygame.K_SPACE):
                # Fix: Handle different menu options properly
                selected_option = self.general_options[self.general_index['col'] + self.general_index['row'] * 2]
                if selected_option == '⚔️ Attack':
                    self.state = 'attack'
                elif selected_option == '💚 Heal':
                    # Call heal action immediately
                    if hasattr(self, 'get_input_callback'):
                        self.get_input_callback('heal', None)
                    self.state = 'general'
                elif selected_option == '🔄 Switch':
                    if self.available_monsters:
                        self.state = 'switch'
                    else:
                        self.state = 'general'
                elif selected_option == '🚪 Escape':
                    # Call escape action immediately
                    if hasattr(self, 'get_input_callback'):
                        self.get_input_callback('escape', None)

        elif self.state == 'attack':
            if just_pressed(pygame.K_DOWN):
                self.attack_index['row'] = (self.attack_index['row'] + 1) % self.rows
            if just_pressed(pygame.K_UP):
                self.attack_index['row'] = (self.attack_index['row'] - 1) % self.rows
            if just_pressed(pygame.K_RIGHT):
                self.attack_index['col'] = (self.attack_index['col'] + 1) % self.cols
            if just_pressed(pygame.K_LEFT):
                self.attack_index['col'] = (self.attack_index['col'] - 1) % self.cols
            if just_pressed(pygame.K_SPACE):
                attack = self.monster.abilities[self.attack_index['col'] + self.attack_index['row'] * 2]
                if hasattr(self, 'get_input_callback'):
                    self.get_input_callback('attack', attack)
                self.state = 'general'

        elif self.state == 'switch':
            if self.available_monsters:
                if just_pressed(pygame.K_DOWN):
                    self.switch_index = (self.switch_index + 1) % len(self.available_monsters)
                if just_pressed(pygame.K_UP):
                    self.switch_index = (self.switch_index - 1) % len(self.available_monsters)
                if just_pressed(pygame.K_SPACE):
                    selected_monster = self.available_monsters[self.switch_index]
                    if hasattr(self, 'get_input_callback'):
                        self.get_input_callback('switch', selected_monster)
                    self.state = 'general'
        
        if just_pressed(pygame.K_ESCAPE):
            self.state = 'general'
            self.general_index = {'col': 0, 'row': 0}
            self.attack_index = {'col': 0, 'row': 0}
            self.switch_index = 0
    
    def quad_select(self, index, options):
        """Enhanced menu with gradient backgrounds and animations"""
        self.pulse_timer += 0.05
        
        # Main menu background with gradient
        rect = pygame.Rect(self.left + 40, self.top + 60, 450, 220)
        
        # Create gradient background
        bg_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        for y in range(rect.height):
            alpha = 200 - (y * 50 // rect.height)
            color = (40, 40, 80, alpha)
            pygame.draw.line(bg_surf, color, (0, y), (rect.width, y))
        
        self.display_surface.blit(bg_surf, rect.topleft)
        pygame.draw.rect(self.display_surface, (100, 150, 255), rect, 3, 8)

        # menu with enhanced styling
        for col in range(self.cols):
            for row in range(self.rows):
                x = rect.left + rect.width / (self.cols * 2) + (rect.width / self.cols) * col
                y = rect.top + rect.height / (self.rows * 2) + (rect.height / self.rows) * row
                i = col + 2 * row
                is_selected = (col == index['col'] and row == index['row'])
                
                # Create button background
                btn_width = 180 if len(options[i]) > 15 else 120  # Wider buttons for attack descriptions
                btn_height = 60 if len(options[i]) > 15 else 50
                btn_rect = pygame.Rect(x - btn_width//2, y - btn_height//2, btn_width, btn_height)
                
                if is_selected:
                    # Animated glow for selected item
                    glow_color = (255, 255, 100, 100 + int(50 * math.sin(self.pulse_timer * 3)))
                    glow_surf = pygame.Surface((btn_width + 20, btn_height + 10), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surf, glow_color, (0, 0, btn_width + 20, btn_height + 10), border_radius=8)
                    self.display_surface.blit(glow_surf, (btn_rect.x - 10, btn_rect.y - 5))
                
                # Button background
                btn_color = (80, 120, 200) if is_selected else (60, 60, 100)
                pygame.draw.rect(self.display_surface, btn_color, btn_rect, border_radius=8)
                pygame.draw.rect(self.display_surface, (200, 200, 200), btn_rect, 2, 8)

                # Text
                text_color = (255, 255, 255) if is_selected else (200, 200, 200)
                text_surf = self.font.render(options[i], True, text_color)
                text_rect = text_surf.get_rect(center=(x, y))
                self.display_surface.blit(text_surf, text_rect)

    def switch(self):
        """Enhanced creature switching menu"""
        # Enhanced background
        rect = pygame.Rect(self.left + 40, self.top - 140, 450, 420)
        
        # Gradient background
        bg_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        for y in range(rect.height):
            alpha = 220 - (y * 60 // rect.height)
            color = (30, 60, 30, alpha)
            pygame.draw.line(bg_surf, color, (0, y), (rect.width, y))
        
        self.display_surface.blit(bg_surf, rect.topleft)
        pygame.draw.rect(self.display_surface, (100, 255, 150), rect, 3, 8)
        
        # Title
        title_surf = self.large_font.render("🔄 Switch Creature", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(rect.centerx, rect.top + 30))
        self.display_surface.blit(title_surf, title_rect)

        # menu with creature portraits
        v_offset = 0 if self.switch_index < self.visible_monsters else -(self.switch_index - self.visible_monsters + 1) * rect.height / self.visible_monsters
        for i in range(len(self.available_monsters)):
            creature = self.available_monsters[i]
            x = rect.centerx
            y = rect.top + 80 + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i + v_offset
            
            is_selected = (i == self.switch_index)
            
            # Creature card background
            card_rect = pygame.Rect(x - 150, y - 30, 300, 60)
            card_color = (100, 200, 100) if is_selected else (60, 100, 60)
            pygame.draw.rect(self.display_surface, card_color, card_rect, border_radius=10)
            
            if is_selected:
                pygame.draw.rect(self.display_surface, (255, 255, 100), card_rect, 3, 10)
            
            # Creature portrait
            image_key = CREATURE_IMAGE_MAP.get(creature.name, creature.name)
            if image_key in self.simple_surfs:
                portrait = pygame.transform.scale(self.simple_surfs[image_key], (40, 40))
                portrait_rect = portrait.get_rect(center=(x - 120, y))
                self.display_surface.blit(portrait, portrait_rect)
              # Creature info with fitted text
            text_color = (255, 255, 255) if is_selected else (200, 200, 200)
            fitted_font, fitted_name = self.fit_text_to_box(creature.name, 180, 24)  # Max width 180px
            name_surf = fitted_font.render(fitted_name, True, text_color)
            name_rect = name_surf.get_rect(center=(x - 40, y - 10))
            self.display_surface.blit(name_surf, name_rect)
            
            # Health bar
            hp_text = f"HP: {creature.health}/{creature.max_health}"
            hp_surf = pygame.font.Font(None, 20).render(hp_text, True, text_color)
            hp_rect = hp_surf.get_rect(center=(x - 40, y + 10))
            self.display_surface.blit(hp_surf, hp_rect)
            name = self.available_monsters[i].name

            simple_surf = self.simple_surfs[CREATURE_IMAGE_MAP[name]]  # Use mapping to get correct image
            simple_rect = simple_surf.get_rect(center = (x - 100, y))

            text_surf = self.font.render(name, True, color)
            text_rect = text_surf.get_rect(midleft = (x,y))
            if rect.collidepoint(text_rect.center):
                self.display_surface.blit(text_surf, text_rect)
                self.display_surface.blit(simple_surf, simple_rect)

    def stats(self):
        # bg 
        rect = pygame.Rect(self.left, self.top, 250, 80)
        pygame.draw.rect(self.display_surface, COLORS['white'],rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'],rect, 4, 4)
        
        # data with fitted text
        name_width = rect.width * 0.9  # Use 90% of rect width
        fitted_font, fitted_name = self.fit_text_to_box(self.monster.name, name_width, 28)
        name_surf = fitted_font.render(fitted_name, True, COLORS['black'])
        name_rect = name_surf.get_rect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, 12))
        self.display_surface.blit(name_surf, name_rect)

        # health bar 
        health_rect = pygame.Rect(name_rect.left, name_rect.bottom + 10, rect.width * 0.9, 20)
        pygame.draw.rect(self.display_surface, COLORS['gray'], health_rect)
        self.draw_bar(health_rect, self.monster.health, self.monster.max_health)
    
    def draw_bar(self, rect, value, max_value):
        ratio = rect.width / max_value
        progress_rect = pygame.Rect(rect.topleft, (value * ratio,rect.height))
        pygame.draw.rect(self.display_surface, COLORS['red'], progress_rect)

    def update(self):
        self.input()
        self.available_monsters = [monster for monster in self.player_monsters if monster!= self.monster and monster.health > 0]

    def draw(self):
        if self.state == 'general': 
            self.draw_general_menu()
        elif self.state == 'attack': 
            self.draw_attack_menu()
        elif self.state == 'switch': 
            self.switch()
        
        if self.state != 'switch':
            self.stats()

    def format_attack_name(self, attack_key):
        """Format attack names for better display"""
        # Convert underscore names to proper case
        formatted = attack_key.replace('_', ' ').title()
        return formatted
    
    def get_attack_display_info(self, attack_key):
        """Get formatted attack information for display"""
        attack_data = ATTACK_DATA[attack_key]
        name = self.format_attack_name(attack_key)
        damage = attack_data['damage']
        element = attack_data['element'].title()
        return f"{name} ({element} - {damage} DMG)"

    def handle_action(self, state, data=None):
        """Handle UI input and trigger appropriate game actions"""
        if hasattr(self, 'get_input_callback') and callable(self.get_input_callback):
            self.get_input_callback(state, data)

    def set_input_handler(self, handler):
        """Set the input handler function from the main game"""
        self.input_handler = handler

    def draw_general_menu(self):
        """Draw the main battle menu"""
        self.pulse_timer += 0.05
        
        # Main menu background with gradient
        rect = pygame.Rect(self.left + 40, self.top + 60, 450, 220)
        
        # Create gradient background
        bg_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        for y in range(rect.height):
            alpha = 200 - (y * 50 // rect.height)
            color = (40, 40, 80, alpha)
            pygame.draw.line(bg_surf, color, (0, y), (rect.width, y))
        
        self.display_surface.blit(bg_surf, rect.topleft)
        pygame.draw.rect(self.display_surface, (100, 150, 255), rect, 3, 8)

        # Draw menu options
        for col in range(self.cols):
            for row in range(self.rows):
                x = rect.left + rect.width / (self.cols * 2) + (rect.width / self.cols) * col
                y = rect.top + rect.height / (self.rows * 2) + (rect.height / self.rows) * row
                i = col + 2 * row
                
                if i < len(self.general_options):
                    is_selected = (col == self.general_index['col'] and row == self.general_index['row'])
                    
                    # Create button background
                    btn_width = 180
                    btn_height = 60
                    btn_rect = pygame.Rect(x - btn_width//2, y - btn_height//2, btn_width, btn_height)
                    
                    if is_selected:
                        # Animated glow for selected item
                        glow_color = (255, 255, 100, 100 + int(50 * math.sin(self.pulse_timer * 3)))
                        glow_surf = pygame.Surface((btn_width + 20, btn_height + 10), pygame.SRCALPHA)
                        pygame.draw.rect(glow_surf, glow_color, (0, 0, btn_width + 20, btn_height + 10), border_radius=8)
                        self.display_surface.blit(glow_surf, (btn_rect.x - 10, btn_rect.y - 5))
                    
                    # Button background
                    btn_color = (80, 120, 200) if is_selected else (60, 60, 100)
                    pygame.draw.rect(self.display_surface, btn_color, btn_rect, border_radius=8)
                    pygame.draw.rect(self.display_surface, (200, 200, 200), btn_rect, 2, 8)                    # Text with automatic sizing
                    text_color = (255, 255, 255) if is_selected else (200, 200, 200)
                    fitted_font, fitted_text = self.fit_text_to_box(self.general_options[i], btn_width - 10, 24)
                    text_surf = fitted_font.render(fitted_text, True, text_color)
                    text_rect = text_surf.get_rect(center=(x, y))
                    self.display_surface.blit(text_surf, text_rect)

    def draw_attack_menu(self):
        """Draw the attack selection menu"""
        self.pulse_timer += 0.05
        
        # Attack menu background with gradient
        rect = pygame.Rect(self.left + 40, self.top + 60, 450, 220)
        
        # Create gradient background
        bg_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        for y in range(rect.height):
            alpha = 220 - (y * 60 // rect.height)
            color = (60, 20, 20, alpha)
            pygame.draw.line(bg_surf, color, (0, y), (rect.width, y))
        
        self.display_surface.blit(bg_surf, rect.topleft)
        pygame.draw.rect(self.display_surface, (200, 100, 100), rect, 3, 8)

        # Draw attack options
        for col in range(self.cols):
            for row in range(self.rows):
                x = rect.left + rect.width / (self.cols * 2) + (rect.width / self.cols) * col
                y = rect.top + rect.height / (self.rows * 2) + (rect.height / self.rows) * row
                i = col + 2 * row
                
                if i < len(self.monster.abilities):
                    attack_key = self.monster.abilities[i]
                    attack_info = self.get_attack_display_info(attack_key)
                    is_selected = (col == self.attack_index['col'] and row == self.attack_index['row'])
                    
                    # Create button background
                    btn_width = 200
                    btn_height = 70
                    btn_rect = pygame.Rect(x - btn_width//2, y - btn_height//2, btn_width, btn_height)
                    
                    if is_selected:
                        # Animated glow for selected item
                        glow_color = (255, 100, 100, 100 + int(50 * math.sin(self.pulse_timer * 3)))
                        glow_surf = pygame.Surface((btn_width + 20, btn_height + 10), pygame.SRCALPHA)
                        pygame.draw.rect(glow_surf, glow_color, (0, 0, btn_width + 20, btn_height + 10), border_radius=8)
                        self.display_surface.blit(glow_surf, (btn_rect.x - 10, btn_rect.y - 5))
                    
                    # Button background with element color
                    if attack_key in ATTACK_DATA:
                        element = ATTACK_DATA[attack_key]['element']
                        element_color = self.element_colors.get(element, (100, 100, 100))
                        if is_selected:
                            btn_color = tuple(min(255, c + 30) for c in element_color)
                        else:
                            btn_color = tuple(max(0, c - 30) for c in element_color)
                    else:
                        btn_color = (80, 120, 200) if is_selected else (60, 60, 100)
                    
                    pygame.draw.rect(self.display_surface, btn_color, btn_rect, border_radius=8)
                    pygame.draw.rect(self.display_surface, (200, 200, 200), btn_rect, 2, 8)                    # Attack text with automatic sizing and wrapping
                    text_color = (255, 255, 255) if is_selected else (200, 200, 200)
                    wrap_font, text_lines = self.wrap_text(attack_info, btn_width - 10, 18)
                    
                    # Draw multiple lines if needed
                    line_height = wrap_font.get_height()
                    total_height = len(text_lines) * line_height
                    start_y = y - (total_height // 2)
                    
                    for idx, line in enumerate(text_lines):
                        text_surf = wrap_font.render(line, True, text_color)
                        text_rect = text_surf.get_rect(center=(x, start_y + idx * line_height))
                        self.display_surface.blit(text_surf, text_rect)

    def fit_text_to_box(self, text, max_width, font_size=24):
        """Fit text to a specific width by adjusting font size or truncating"""
        # Try different font sizes
        for size in range(font_size, 12, -2):  # Start from font_size, go down to 12
            test_font = pygame.font.Font(None, size)
            text_surf = test_font.render(text, True, (255, 255, 255))
            if text_surf.get_width() <= max_width:
                return test_font, text
        
        # If still too long, truncate text
        small_font = pygame.font.Font(None, 14)
        while len(text) > 0:
            text_surf = small_font.render(text + "...", True, (255, 255, 255))
            if text_surf.get_width() <= max_width:
                return small_font, text + "..."
            text = text[:-1]
        
        return small_font, "..."

    def wrap_text(self, text, max_width, font_size=20):
        """Wrap text to multiple lines if needed"""
        font = pygame.font.Font(None, font_size)
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_surf = font.render(test_line, True, (255, 255, 255))
            
            if test_surf.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return font, lines

class OpponentUI:
    def __init__(self, monster, opponent_index=0, total_opponents=4):
        self.display_surface = pygame.display.get_surface()
        self.monster = monster
        self.font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 20)
        self.opponent_index = opponent_index
        self.total_opponents = total_opponents
    
    def fit_text_to_box(self, text, max_width, font_size=30):
        """Fit text to a specific width by adjusting font size"""
        for size in range(font_size, 12, -2):
            test_font = pygame.font.Font(None, size)
            text_surf = test_font.render(text, True, COLORS['black'])
            if text_surf.get_width() <= max_width:
                return test_font, text
        
        # If still too long, truncate
        small_font = pygame.font.Font(None, 14)
        while len(text) > 0:
            text_surf = small_font.render(text + "...", True, COLORS['black'])
            if text_surf.get_width() <= max_width:
                return small_font, text + "..."
            text = text[:-1]
        
        return small_font, "..."
    
    def draw(self):
        # bg 
        rect = pygame.Rect((0,0), (250,100))  # Made slightly taller for team info
        rect.midleft = (500, self.monster.rect.centery)
        pygame.draw.rect(self.display_surface, COLORS['white'],rect, 0, 4)
        pygame.draw.rect(self.display_surface, COLORS['gray'],rect, 4, 4)

        # name with fitted text
        name_width = rect.width * 0.9  # Use 90% of rect width
        fitted_font, fitted_name = self.fit_text_to_box(self.monster.name, name_width, 30)
        name_surf = fitted_font.render(fitted_name, True, COLORS['black'])
        name_rect = name_surf.get_rect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, 8))
        self.display_surface.blit(name_surf, name_rect)        # Team progress indicator
        team_text = f"Opponent {self.opponent_index + 1}/{self.total_opponents}"
        team_surf = self.small_font.render(team_text, True, COLORS['black'])
        team_rect = team_surf.get_rect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.05, name_rect.bottom + 2))
        self.display_surface.blit(team_surf, team_rect)
        
        # health bar - positioned inside the box
        health_rect = pygame.Rect(name_rect.left, team_rect.bottom + 5, rect.width * 0.9, 15)
        # Ensure health bar stays inside the box
        max_right = rect.right - 12  # Leave some margin from box edge
        if health_rect.right > max_right:
            health_rect.width = max_right - health_rect.left
        
        pygame.draw.rect(self.display_surface, COLORS['gray'], health_rect)
        ratio = health_rect.width / self.monster.max_health
        progress_rect = pygame.Rect(health_rect.topleft, (self.monster.health * ratio, health_rect.height))
        pygame.draw.rect(self.display_surface, COLORS['red'], progress_rect)

class CreatureSelection:
    """
    Enhanced creature selection screen - allows player to choose 4 creatures from all available
    Features attractive UI with animations, gradients, and visual effects
    """
    def __init__(self, simple_surfs):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 56)
        self.large_font = pygame.font.Font(None, 32)
        self.simple_surfs = simple_surfs
        
        # All available creatures
        self.all_creatures = list(CREATURE_DATA.keys())
        self.selected_creatures = []  # Player's chosen creatures (max 4)
        self.current_index = 0  # Currently highlighted creature
        
        # Enhanced UI layout
        self.creatures_per_row = 6
        self.creature_size = 90
        self.spacing = 25
        self.start_x = 120
        self.start_y = 180
        
        # Animation variables
        self.hover_scale = 1.0
        self.hover_target = 1.0
        self.pulse_timer = 0
        self.float_offset = 0
        
        # Color palette for elements
        self.element_colors = {
            'flame': (255, 100, 100),   # Red
            'aqua': (100, 150, 255),    # Blue  
            'nature': (100, 255, 100), # Green
            'normal': (200, 200, 200)  # Gray
        }
          # Key tracking for input
        self.previous_keys = pygame.key.get_pressed()
        self.current_keys = pygame.key.get_pressed()
    
    def fit_text_to_box(self, text, max_width, font_size=24):
        """Fit text to a specific width by adjusting font size"""
        for size in range(font_size, 12, -2):
            test_font = pygame.font.Font(None, size)
            text_surf = test_font.render(text, True, (255, 255, 255))
            if text_surf.get_width() <= max_width:
                return test_font, text
        
        # If still too long, truncate
        small_font = pygame.font.Font(None, 14)
        while len(text) > 0:
            text_surf = small_font.render(text + "...", True, (255, 255, 255))
            if text_surf.get_width() <= max_width:
                return small_font, text + "..."
            text = text[:-1]
        
        return small_font, "..."
    
    def handle_input(self):
        """Handle keyboard input for creature selection"""
        # Update key states
        self.previous_keys = self.current_keys
        self.current_keys = pygame.key.get_pressed()
        
        def just_pressed(key):
            return self.current_keys[key] and not self.previous_keys[key]
        
        # Navigation
        if just_pressed(pygame.K_RIGHT):
            self.current_index = (self.current_index + 1) % len(self.all_creatures)
        elif just_pressed(pygame.K_LEFT):
            self.current_index = (self.current_index - 1) % len(self.all_creatures)
        elif just_pressed(pygame.K_DOWN):
            new_index = self.current_index + self.creatures_per_row
            if new_index < len(self.all_creatures):
                self.current_index = new_index
        elif just_pressed(pygame.K_UP):
            new_index = self.current_index - self.creatures_per_row
            if new_index >= 0:
                self.current_index = new_index
        
        # Selection
        elif just_pressed(pygame.K_SPACE) or just_pressed(pygame.K_RETURN):
            current_creature = self.all_creatures[self.current_index]
            
            if current_creature in self.selected_creatures:
                # Deselect if already selected
                self.selected_creatures.remove(current_creature)
            elif len(self.selected_creatures) < 4:
                # Select if under limit
                self.selected_creatures.append(current_creature)
        
        # Confirm selection
        elif just_pressed(pygame.K_c) and len(self.selected_creatures) == 4:
            return True  # Selection complete        
        return False  # Still selecting
    
    def draw(self):
        """Draw the enhanced creature selection screen with animations and visual effects"""
        # Animated background gradient
        self.pulse_timer += 0.02
        self.float_offset += 0.01
        
        # Create gradient background
        for y in range(WINDOW_HEIGHT):
            # Create a smooth gradient from dark blue to dark purple
            r = int(20 + 10 * math.sin(self.pulse_timer + y * 0.01))
            g = int(25 + 15 * math.sin(self.pulse_timer * 1.5 + y * 0.01))
            b = int(60 + 20 * math.sin(self.pulse_timer * 0.8 + y * 0.01))
            color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
            pygame.draw.line(self.display_surface, color, (0, y), (WINDOW_WIDTH, y))
        
        # Animated title with glow effect
        title_text = "🌟 Choose Your Elemental Team 🌟"
        
        # Draw title shadow/glow
        for offset in [(2, 2), (1, 1), (0, 0)]:
            shadow_color = (100, 50, 150) if offset != (0, 0) else (255, 255, 255)
            title_surf = self.title_font.render(title_text, True, shadow_color)
            title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2 + offset[0], 70 + offset[1]))
            self.display_surface.blit(title_surf, title_rect)
        
        # Animated subtitle
        subtitle_text = "Select 4 Creatures for Battle"
        float_y = 110 + math.sin(self.pulse_timer * 2) * 3
        subtitle_surf = self.large_font.render(subtitle_text, True, (200, 220, 255))
        subtitle_rect = subtitle_surf.get_rect(center=(WINDOW_WIDTH // 2, float_y))
        self.display_surface.blit(subtitle_surf, subtitle_rect)
        
        # Enhanced instructions with icons
        selected_count = len(self.selected_creatures)
        progress_color = (100, 255, 100) if selected_count == 4 else (255, 200, 100)
        instruction_text = f"🎯 Selected: {selected_count}/4  •  ⌨️ SPACE: Select  •  ✅ C: Confirm"
        inst_surface = self.font.render(instruction_text, True, progress_color)
        inst_rect = inst_surface.get_rect(center=(WINDOW_WIDTH // 2, 140))
        self.display_surface.blit(inst_surface, inst_rect)
        
        # Update hover animation
        if self.current_index < len(self.all_creatures):
            self.hover_target = 1.15
        else:
            self.hover_target = 1.0
        self.hover_scale += (self.hover_target - self.hover_scale) * 0.15
        
        # Draw creatures grid with enhanced visuals
        for i, creature_name in enumerate(self.all_creatures):
            row = i // self.creatures_per_row
            col = i % self.creatures_per_row
            
            x = self.start_x + col * (self.creature_size + self.spacing)
            y = self.start_y + row * (self.creature_size + self.spacing * 2)
            
            # Calculate scale and floating effect
            scale = self.hover_scale if i == self.current_index else 1.0
            float_y_offset = math.sin(self.float_offset + i * 0.5) * 2 if i == self.current_index else 0
            
            actual_size = int(self.creature_size * scale)
            actual_x = x - (actual_size - self.creature_size) // 2
            actual_y = y - (actual_size - self.creature_size) // 2 + float_y_offset
            
            # Get creature data for styling
            creature_data = CREATURE_DATA[creature_name]
            element_color = self.element_colors.get(creature_data['element'], (200, 200, 200))
            
            # Draw selection background glow
            if creature_name in self.selected_creatures:
                glow_size = actual_size + 20
                glow_surf = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (*element_color, 80), (glow_size//2, glow_size//2), glow_size//2)
                self.display_surface.blit(glow_surf, (actual_x - 10, actual_y - 10))
            
            # Draw main creature background
            bg_rect = pygame.Rect(actual_x, actual_y, actual_size, actual_size)
            
            # Create gradient background for creature card
            bg_surf = pygame.Surface((actual_size, actual_size), pygame.SRCALPHA)
            for py in range(actual_size):
                alpha = 255 - (py * 100 // actual_size)
                color = (*element_color, max(50, alpha))
                pygame.draw.line(bg_surf, color, (0, py), (actual_size, py))
            
            self.display_surface.blit(bg_surf, (actual_x, actual_y))
            
            # Draw creature image
            image_key = CREATURE_IMAGE_MAP.get(creature_name, creature_name)
            if image_key in self.simple_surfs:
                creature_surf = pygame.transform.scale(self.simple_surfs[image_key], 
                                                     (actual_size - 10, actual_size - 10))
                creature_rect = creature_surf.get_rect(center=bg_rect.center)
                self.display_surface.blit(creature_surf, creature_rect)
            
            # Draw borders and highlights
            border_color = (255, 255, 255) if i == self.current_index else element_color
            border_width = 4 if i == self.current_index else 2
            pygame.draw.rect(self.display_surface, border_color, bg_rect, border_width)
            
            # Selection indicator
            if creature_name in self.selected_creatures:
                check_surf = self.large_font.render("✓", True, (255, 255, 255))
                check_rect = check_surf.get_rect(topright=(bg_rect.right - 5, bg_rect.top + 5))
                # Draw check mark background
                pygame.draw.circle(self.display_surface, (0, 200, 0), check_rect.center, 15)
                self.display_surface.blit(check_surf, check_rect)
              # Draw creature name with shadow and text fitting
            name_y = actual_y + actual_size + 8
            name_width = self.creature_size + self.spacing  # Max width for name
            fitted_font, fitted_name = self.fit_text_to_box(creature_name, name_width, 24)
            
            # Shadow
            name_shadow = fitted_font.render(fitted_name, True, (0, 0, 0))
            shadow_rect = name_shadow.get_rect(center=(x + self.creature_size // 2 + 1, name_y + 1))
            self.display_surface.blit(name_shadow, shadow_rect)
            # Main text
            name_surf = fitted_font.render(fitted_name, True, (255, 255, 255))
            name_rect = name_surf.get_rect(center=(x + self.creature_size // 2, name_y))
            self.display_surface.blit(name_surf, name_rect)
            
            # Draw creature stats with element color
            stats_text = f"{creature_data['element'].title()} • {creature_data['health']}HP"
            stats_surf = pygame.font.Font(None, 18).render(stats_text, True, element_color)
            stats_rect = stats_surf.get_rect(center=(x + self.creature_size // 2, name_y + 20))
            self.display_surface.blit(stats_surf, stats_rect)
        
        # Draw progress bar at bottom
        self.draw_progress_bar()
    
    def draw_progress_bar(self):
        """Draw a fancy progress bar showing selection progress"""
        bar_width = 400
        bar_height = 20
        bar_x = (WINDOW_WIDTH - bar_width) // 2
        bar_y = WINDOW_HEIGHT - 80
        
        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.display_surface, (50, 50, 50), bg_rect)
        pygame.draw.rect(self.display_surface, (200, 200, 200), bg_rect, 2)
        
        # Progress fill
        progress = len(self.selected_creatures) / 4
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            progress_rect = pygame.Rect(bar_x, bar_y, progress_width, bar_height)
            color = (100, 255, 100) if progress == 1.0 else (255, 200, 100)
            pygame.draw.rect(self.display_surface, color, progress_rect)
        
        # Progress text
        progress_text = f"{len(self.selected_creatures)}/4 Creatures Selected"
        if len(self.selected_creatures) == 4:
            progress_text += " - Press C to Confirm!"
        
        text_surf = self.font.render(progress_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, bar_y + bar_height + 15))
        self.display_surface.blit(text_surf, text_rect)