from settings import * 
import os

def folder_importer(*path):
    surfs = {}
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = join(base_dir, *path)
    
    for folder_path, _, file_names in walk(full_path):
        for file_name in file_names:
            file_path = join(folder_path, file_name)
            try:
                surfs[file_name.split('.')[0]] = pygame.image.load(file_path).convert_alpha()
            except pygame.error as e:
                print(f"Warning: Could not load image {file_name}: {e}")
    return surfs

def audio_importer(*path):
    audio_dict = {}
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = join(base_dir, *path)
    
    for folder_path, _, file_names in walk(full_path):
        for file_name in file_names:
            file_path = join(folder_path, file_name)
            try:
                audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(file_path)
            except pygame.error as e:
                print(f"Warning: Could not load audio file {file_name}: {e}")
    return audio_dict

def tile_importer(cols, *path):
    attack_frames = {}
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = join(base_dir, *path)
    
    for folder_path, _, file_names in walk(full_path):
        for file_name in file_names:
            file_path = join(folder_path, file_name)
            try:
                surf = pygame.image.load(file_path).convert_alpha()
                attack_frames[file_name.split('.')[0]] = []
                cutout_width = surf.get_width() / cols
                for col in range(cols):
                    cutout_surf = pygame.Surface((cutout_width, surf.get_height()), pygame.SRCALPHA)
                    cutout_rect = pygame.Rect(cutout_width * col,0,cutout_width,surf.get_height())
                    cutout_surf.blit(surf, (0,0),cutout_rect)
                    attack_frames[file_name.split('.')[0]].append(cutout_surf)
            except pygame.error as e:
                print(f"Warning: Could not load attack animation {file_name}: {e}")
    return attack_frames