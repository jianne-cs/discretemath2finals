# Ave Mujica - Logic Grimoire

An interactive desktop application that teaches formal logic through the narrative of Ave Mujica (a fictional band). Learn 16 fundamental logical operations through character-driven quests and truth table puzzles.

## Features

- **4 Main Sections**: Intro, Truth Cathedral, Character Encounters, 16 Gates
- **5 Character Quests**: Each character represents a logical operation
- **16 Gates of Truth**: Interactive puzzles to unlock songs
- **Music Player**: Background music that unlocks as you progress
- **Progress Tracking**: Save/load your progress automatically
- **Secret Ending**: Unlock by completing all quests and gates

## Screenshots

*Add your screenshots here*

## Requirements

- Python 3.11+ (Python 3.14 supported with pygame-ce)
- pygame or pygame-ce
- Pillow (PIL)

## Installation

### 1. Clone/Download the Project

```bash
git clone <repository-url>
cd dm2finals
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install pygame-ce
pip install Pillow
```

*Note: Use `pygame-ce` for Python 3.14+. For older Python versions, use `pip install pygame`.*

### 5. Run the Application

**Option A: Using system Python directly**
```bash
C:\Python314\python.exe main.py
```

**Option B: Using virtual environment Python**
```bash
python main.py
```

*Note: If `python` doesn't work in your terminal, use `C:\Python314\python.exe main.py` instead.*

## How to Play

### Navigation
- Use the navigation buttons at the bottom: **Truth Cathedral**, **Character Quests**, **16 Gates**, **Quest Hub**
- Keyboard shortcuts: 1-4 for sections, Arrow keys for navigation

### Character Quests

Each character represents a logical operation:

| Character | Role | Operation |
|-----------|------|-----------|
| Sakiko Togawa | Oblivionis | Implication (→) |
| Uika Misumi | Doloris | XOR (⊕) |
| Mutsumi Wakaba | Mortis | Negation (¬) |
| Umiri Yahata | Timoris | NOR (↓) |
| Nyamu Yūtenji | Amoris | NAND (↑) |

**Quest Flow:**
1. Click "Begin Quest" on a character's card
2. Read the story dialogue
3. Complete truth table puzzles
4. Advance through 3 stages per quest
5. Unlock the character's song upon completion

### 16 Gates of Truth

- Click on a gate to practice its truth table
- Correctly identify the operation to unlock its song
- Complete all 16 to unlock the True Secret Ending

### Music Player

The music player at the bottom features:
- **▶ Play/Pause**: Start or pause music
- **⏮ ⏭**: Previous/Next track
- **Volume**: Adjust playback volume

**Music Unlock System:**
| Action | Reward |
|--------|--------|
| Complete character quest | Character's song added to playlist |
| Complete 16 Gates puzzle | Gate's song added to playlist |
| Complete all quests + all gates | Secret Ending song unlocked |

### Secret Ending

To unlock the True Secret Ending:
1. Complete all 5 character quests
2. Complete all 16 Gates of Truth
3. The final quest will reveal the secret ending

## Project Structure

```
dm2finals/
├── main.py                 # Entry point
├── gui_components.py        # Main application class
├── quest_system.py         # Quest management system
├── character_quests.py     # Character quest definitions
├── tutorial.py            # Logic tutorial content
├── config.py              # Color scheme configuration
├── assets/
│   ├── images/            # Character images
│   └── music/
│       ├── main webpage/  # Default background music
│       ├── character quests songs/  # Unlockable character songs
│       └── 16 gates unlocked songs/ # Unlockable gate songs
├── .venv/                 # Virtual environment
└── quest_progress.json    # Saved progress
```

## Character Songs

| Character | Song Unlocked |
|-----------|--------------|
| Sakiko Togawa | Masquerade Rhapsody Request |
| Uika Misumi | Angles |
| Mutsumi Wakaba | Choir 'S' Choir |
| Umiri Yahata | 'S/' The Way |
| Nyamu Yūtenji | Blue Eyes |
| Secret Ending | Kamisama Baka |

## 16 Gate Songs

| Gate | Operation | Song |
|------|-----------|------|
| 1 | NAND | Ave Mujica |
| 2 | XOR | KiLLKiSS |
| 3 | XNOR | georgette me, georgette you |
| 4 | OR | Kuro no Birthday |
| 5 | AND | Sophie |
| 6 | Implication | Crucifix X |
| 7 | NOR | Deep Into The Forest |
| 8-11 | Symbol Series | Symbol I-IV |
| 12 | Contradiction | Imprisoned XII |
| 13 | Tautology | Octagram Dance |
| 14 | Projection Q | DIVINE |
| 15 | Projection P | Alter Ego |
| 16 | Negation of Q | Ether |

## Troubleshooting

**pygame not found error:**
```bash
pip install pygame-ce
```

**Virtual environment Python incompatible:**
```bash
C:\Python314\python.exe -m pip install pygame-ce Pillow
```

**Music not playing:**
- Check that music files are in the correct folders
- Ensure pygame-ce is installed

## Resetting Progress

To start fresh:
1. Close the application
2. Delete `quest_progress.json` from the project folder
3. Restart the application

## Credits

- Ave Mujica Logic Grimoire
- Inspired by Ave Mujica lore
- Built with Python 3 + Tkinter + Pygame

## License

