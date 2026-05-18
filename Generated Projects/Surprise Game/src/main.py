import pygame
import json
import random
import time
import os
from pathlib import Path

# ------------------------------------------------------------
# Configuration loading
# ------------------------------------------------------------
CONFIG_PATH = Path(__file__).parent / 'config.json'
with open(CONFIG_PATH) as f:
    cfg = json.load(f)

WIDTH = cfg['maze_width']
HEIGHT = cfg['maze_height']
TILE_SIZE = cfg['tile_size']
QUANTUM_DURATION = cfg['quantum_duration']
QUANTUM_COOLDOWN = cfg['quantum_cooldown']
PLAYER_SPEED = cfg['player_speed']
BG_COLOR = tuple(cfg['background_color'])

# ------------------------------------------------------------
# Helper functions for maze generation (recursive backtracker)
# ------------------------------------------------------------

def carve_passages_from(cx, cy, grid, visited):
    """Carve passages using depth‑first search.
    grid: 2D list of booleans, True = floor, False = wall
    visited: set of (x, y) tuples
    """
    dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
    random.shuffle(dirs)
    visited.add((cx, cy))
    grid[cy][cx] = True  # mark current cell as floor
    for dx, dy in dirs:
        nx, ny = cx + dx, cy + dy
        if 0 < nx < WIDTH and 0 < ny < HEIGHT and (nx, ny) not in visited:
            # knock down wall between cells
            grid[cy + dy // 2][cx + dx // 2] = True
            carve_passages_from(nx, ny, grid, visited)


def generate_maze():
    # Initialize all cells as walls
    grid = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
    visited = set()
    # start from an odd coordinate to ensure walls around
    start_x = random.randrange(1, WIDTH, 2)
    start_y = random.randrange(1, HEIGHT, 2)
    carve_passages_from(start_x, start_y, grid, visited)
    return grid

# ------------------------------------------------------------
# Game classes
# ------------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, images):
        super().__init__()
        self.image = images['player']
        self.rect = self.image.get_rect(topleft=pos)
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED

    def update(self, dt, walls, quantum_active):
        keys = pygame.key.get_pressed()
        self.vel.x = self.vel.y = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel.y = 1
        if self.vel.length_squared() != 0:
            self.vel = self.vel.normalize() * self.speed * dt
            new_rect = self.rect.move(self.vel.x, self.vel.y)
            # Collision detection only with the *active* maze walls
            if not self.collides_with_walls(new_rect, walls):
                self.rect = new_rect

    def collides_with_walls(self, rect, walls):
        # Simple pixel‑perfect check: if any corner is inside a wall tile, block movement
        for corner in [(rect.left, rect.top), (rect.right, rect.top),
                       (rect.left, rect.bottom), (rect.right, rect.bottom)]:
            tx = int(corner[0] // TILE_SIZE)
            ty = int(corner[1] // TILE_SIZE)
            if 0 <= tx < WIDTH and 0 <= ty < HEIGHT:
                if not walls[ty][tx]:  # wall == False
                    return True
        return False

# ------------------------------------------------------------
# Main game function
# ------------------------------------------------------------

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE))
    pygame.display.set_caption('Quantum Maze')
    clock = pygame.time.Clock()

    # Load assets
    asset_path = Path(__file__).parents[1] / 'assets'
    images = {
        'player': pygame.image.load(str(asset_path / 'player.png')).convert_alpha(),
        'wall': pygame.image.load(str(asset_path / 'wall.png')).convert(),
        'floor': pygame.image.load(str(asset_path / 'floor.png')).convert()
    }
    # jump_sound = pygame.mixer.Sound(str(asset_path / 'jump.wav'))
    # Background music (loop)
    # Generate two separate mazes
    maze_current = generate_maze()
    maze_alternate = generate_maze()

    # Player starts at top‑left open cell of current maze
    def find_start(maze):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if maze[y][x]:
                    return x * TILE_SIZE, y * TILE_SIZE
        return 0, 0
    player = Player(find_start(maze_current), images)
    all_sprites = pygame.sprite.Group(player)

    # Timing variables for quantum mechanic
    quantum_active = False
    quantum_timer = 0
    cooldown_timer = 0

    start_time = time.time()
    font = pygame.font.SysFont(None, 24)

    running = True
    while running:
        dt = clock.tick(60) / 1000  # delta time in seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not quantum_active and cooldown_timer <= 0:
                    # Activate quantum jump
                    quantum_active = True
                    quantum_timer = QUANTUM_DURATION
                    cooldown_timer = QUANTUM_COOLDOWN

        # Update quantum timers
        if quantum_active:
            quantum_timer -= dt
            if quantum_timer <= 0:
                quantum_active = False
        else:
            if cooldown_timer > 0:
                cooldown_timer -= dt

        # Choose which maze is currently "solid"
        active_maze = maze_alternate if quantum_active else maze_current

        # Update player
        player.update(dt, active_maze, quantum_active)

        # Rendering
        screen.fill(BG_COLOR)
        # Draw floor and walls
        for y in range(HEIGHT):
            for x in range(WIDTH):
                tile = active_maze[y][x]
                pos = (x * TILE_SIZE, y * TILE_SIZE)
                if tile:
                    screen.blit(images['floor'], pos)
                else:
                    screen.blit(images['wall'], pos)
        all_sprites.draw(screen)

        # UI – elapsed time and quantum cooldown
        elapsed = time.time() - start_time
        score = int(10000 / (elapsed + 1) + WIDTH * HEIGHT)
        ui_text = f"Time: {elapsed:.1f}s  Score: {score}"
        if cooldown_timer > 0 and not quantum_active:
            ui_text += f"  Quantum ready in: {cooldown_timer:.1f}s"
        else:
            ui_text += "  Quantum ready! (Press SPACE)"
        txt_surf = font.render(ui_text, True, (255, 255, 255))
        screen.blit(txt_surf, (5, 5))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
