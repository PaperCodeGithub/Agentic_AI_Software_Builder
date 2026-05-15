from ursina import *

# Initialize the Ursina app
app = Ursina()

# Settings
move_speed = 5          # Units per second
jump_speed = 8          # Initial upward velocity when jumping
gravity = -9.81         # Gravity acceleration (units per second squared)

# Create the ground plane
ground = Entity(
    model='plane',
    scale=(10, 1, 10),
    texture='white_cube',
    texture_scale=(10, 10),
    color=color.gray,
    collider='box'
)

# Create the player cube
player = Entity(
    model='cube',
    color=color.orange,
    scale=(1, 2, 1),            # Make the cube a bit taller for better feel
    position=(0, 1, 0),        # Start slightly above the ground (half height)
    collider='box',
)
# Add a custom attribute to track vertical velocity
player.velocity_y = 0

# Camera follows the player from behind
camera.parent = player
camera.position = (0, 5, -10)
camera.rotation = (30, 0, 0)


def update():
    """Called every frame – handles movement, jumping and simple gravity."""
    # --- Horizontal movement ------------------------------------------------
    direction = Vec3(
        (held_keys['d'] - held_keys['a']),
        0,
        (held_keys['w'] - held_keys['s'])
    )
    if direction != Vec3.zero:
        direction = direction.normalized()
        player.position += direction * move_speed * time.dt
        # Rotate the player to face the movement direction (optional)
        player.rotation_y = direction.angle_zxy

    # --- Simple ground check -------------------------------------------------
    # Cast a short ray downwards to see if we're standing on something.
    ray = raycast(player.world_position, Vec3(0, -1, 0), distance=player.y + 0.1, ignore=[player])
    on_ground = ray.hit

    # --- Jumping ------------------------------------------------------------
    if on_ground:
        # Stick to the ground (prevent sinking due to numerical errors)
        if player.velocity_y < 0:
            player.velocity_y = 0
        if held_keys['space']:
            player.velocity_y = jump_speed
    else:
        # Apply gravity when in the air
        player.velocity_y += gravity * time.dt

    # Apply vertical motion
    player.y += player.velocity_y * time.dt

    # Prevent the player from falling through the ground
    if player.y < 1:  # because the cube's half‑height is 1
        player.y = 1
        player.velocity_y = 0

# Run the app
app.run()
