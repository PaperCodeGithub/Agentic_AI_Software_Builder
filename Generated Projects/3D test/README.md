# Simple 3D Cube Game (Ursina)

A minimal 3D game built with the **Ursina** engine. It demonstrates:
- A controllable player cube that can move forward/backward/left/right.
- Jumping with basic physics (gravity & ground detection).
- Simple camera that follows the player.

## Prerequisites

- **Python 3.8+** (https://www.python.org/downloads/)
- **Git** (optional, for cloning the repository)

## Installation & Running

### Linux / macOS

```bash
# Make the launch script executable (only needed once)
chmod +x run.sh

# Run the helper script which installs dependencies and starts the game
./run.sh
```

### Windows

Double‑click `run.bat` or run it from a Command Prompt:

```cmd
run.bat
```

Both scripts will:
1. Upgrade `pip`.
2. Install the required Python package (`ursina`).
3. Launch `main.py` which starts the game.

## Controls

| Key | Action |
|-----|--------|
| **W** | Move forward |
| **S** | Move backward |
| **A** | Move left |
| **D** | Move right |
| **Space** | Jump |

The camera follows the player from a slightly elevated behind‑the‑back view.

## Project Structure

- `main.py` – Core game code.
- `requirements.txt` – Python dependencies.
- `run.sh` / `run.bat` – Convenience launch scripts.
- `README.md` – This file.

## Extending the Game

The repository is intentionally simple. You can extend it by:
- Adding textures or custom models (place them in an `assets/` folder and reference them in `main.py`).
- Implementing enemies, collectibles, or a UI.
- Tweaking physics values (speed, jump height, gravity) for a different feel.

Happy coding!
