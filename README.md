# 🎮 Elemental Creatures Battle Game

A turn-based creature battle game built with Python and Pygame, featuring strategic combat, creature selection, and a type-based effectiveness system. This project is an educational tool demonstrating key concepts in game development, from object-oriented programming to modern UI design.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

- **⚔️ Strategic Turn-Based Combat**: Engage in battles with a type-effectiveness system (Flame > Nature > Aqua > Flame).
- **🧠 Smart AI Opponent**: The AI strategically chooses attacks based on type advantages and damage output.
- **🎨 18 Unique Creatures**: Collect and battle with a diverse roster of creatures, each with unique elemental types.
- **Interactive Selection Screen**: Choose your team of 4 creatures from a dynamic and visually appealing grid.
- **🏆 Progressive Challenge**: Battle through a team of 5 AI opponents to win the game.
- **✨ Modern UI & Animations**: Features animated backgrounds, element-based color coding, and smooth attack animations.
- **🔄 Restart Functionality**: Easily restart the game after a win or loss to try new strategies.

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- `pip` package manager

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/elemental-creatures-battle.git
    cd elemental-creatures-battle
    ```
    *(Replace `yourusername` with your actual GitHub username)*

2.  **Install dependencies:**
    Create and activate a virtual environment (optional but recommended), then install the required packages.
    ```bash
    # Create a virtual environment
    python -m venv venv
    # Activate it (Windows)
    .\venv\Scripts\activate
    # Or (macOS/Linux)
    # source venv/bin/activate

    # Install packages
    pip install -r requirements.txt
    ```

3.  **Run the game:**

    -   **On Windows:**
        Simply double-click the `run_game.bat` file.

    -   **On other systems (or from the command line):**
        ```bash
        python code/main.py
        ```

## 🎮 How to Play

1.  **Select Your Team**: Use the arrow keys to navigate the creature grid and press `SPACE` to select up to 4 creatures. Press `C` to confirm your team.
2.  **Battle**: Use the arrow keys and `SPACE` to choose your actions:
    -   **Attack**: Select a move to damage the opponent.
    -   **Heal**: Restore 30 HP to your active creature.
    -   **Switch**: Swap your active creature with another from your team.
    -   **Escape**: Quit the game.
3.  **Win/Lose**: Defeat all 5 of the opponent's creatures to win. If all your creatures are defeated, you lose. Press `SPACEBAR` on the end screen to play again.

## 📚 Learning Concepts

This project is a practical demonstration of several key programming and game development concepts:

-   **Object-Oriented Programming (OOP)**: Uses classes for `Game`, `Creature`, `UI`, and `Attack` to create a modular and organized structure.
-   **Game Loop Architecture**: Implements a standard game loop for handling input, updating game state, and rendering graphics.
-   **State Management**: Manages different game states like `selection`, `playing`, `win`, and `lose`.
-   **Data-Driven Design**: Creature stats, attacks, and elemental properties are stored in `settings.py`, making them easy to modify and extend.
-   **AI Algorithm Design**: The opponent's `choose_smart_attack` function provides a simple but effective AI based on type effectiveness and damage.
-   **UI/UX Design**: Includes creating an interactive menu, health bars, and providing clear visual feedback to the player.
-   **Asset Management**: The `support.py` module handles loading and organizing game assets like images and audio.

## 📁 Project Structure

```
elemental-creatures-battle/
├── code/
│   ├── main.py           # Main game loop and core logic
│   ├── settings.py       # Game configuration and data
│   ├── monster.py        # Creature classes and behavior
│   ├── ui.py             # User interface components
│   ├── attack.py         # Attack animations and effects
│   ├── support.py        # Utility functions
│   └── timer.py          # Game timing system
├── images/
│   ├── front/            # Front-facing creature sprites
│   ├── back/             # Back-facing creature sprites
│   ├── simple/           # Simple creature icons
│   ├── attacks/          # Attack animation frames
│   └── other/            # Background and UI elements
├── audio/
│   ├── music.mp3         # Background music
│   └── *.wav             # Sound effects
├── README.md             # This file
├── requirements.txt      # Project dependencies
└── run_game.bat          # Windows script to run the game
```


