import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 512
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pigeon on the Seine")

# Frame rate setup
clock = pygame.time.Clock()
FPS = 60

# Constants for the baguette
OBSTACLE_WIDTH = 119
OBSTACLE_HEIGHT = 512
GAP_HEIGHT = 240          # space between top and bottom baguette
SPAWN_INTERVAL = 1500     # milliseconds
OBSTACLE_SPEED = 3

# Load high score from file if it exists
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        try:
            high_score = int(file.read())
        except:
            high_score = 0

# Load background layers:
def load_scaled(path, size=(WIDTH, HEIGHT)):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)

bg_layers = {
    "sky": load_scaled("assets/background/sky.png"),
    "city": load_scaled("assets/background/city.png"),
    "quais": load_scaled("assets/background/quais.png"),
}

# Parallax scroll speeds for each layer
scroll_speeds = {
    "sky": 0.2,    # very slow (far back)
    "city": 0.5,   # medium (middle distance)
    "quais": 1.0   # full speed (foreground)
}

# Global scroll position
scroll_x = 0

# loading the baguette image
baguette_img = pygame.image.load("assets/obstacles/baguette.png").convert_alpha()
baguette_img_top = pygame.transform.flip(baguette_img, False, True)

# creates an obstacle list
obstacles = []
last_spawn_time = pygame.time.get_ticks()

# Load pigeon tileset
pigeon_sheet = pygame.image.load("assets/pigeon/pigeon_tileset.png").convert_alpha()

# Extract 6 animation frames of the pigeon
pigeon_frames = []
for i in range(6):
    frame = pigeon_sheet.subsurface(pygame.Rect(i * 128, 0, 128, 128))
    pigeon_frames.append(frame) 

# Pigeon variables
pigeon_index = 0
pigeon_anim_timer = 0
PIGEON_ANIM_SPEED = 100  # ms between frames
# Gravity & jump settings
pigeon_velocity = 0
GRAVITY = 0.5
JUMP_STRENGTH = -10
# Pigeon position
pigeon_x = 200
pigeon_y = HEIGHT // 2

#score
score = 0
high_score = 0
font = pygame.font.Font(None, 36)  # default font, size 36


# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pigeon_velocity = JUMP_STRENGTH


    # Update scroll position
    scroll_x += 2  # scrolling speed

    # Draw background layers with parallax effect
    for layer_name in ["sky", "city", "quais"]:
        layer = bg_layers[layer_name]
        speed = scroll_speeds[layer_name]

        # Calculate relative scroll position for the current layer
        rel_x = -(scroll_x * speed) % layer.get_width()

        # Draw two copies of the layer to ensure seamless looping
        screen.blit(layer, (rel_x, 0))
        screen.blit(layer, (rel_x - layer.get_width(), 0))

    current_time = pygame.time.get_ticks()

    if current_time - last_spawn_time > SPAWN_INTERVAL:
        last_spawn_time = current_time

        # Randomize vertical position of the gap
        gap_y = random.randint(100, HEIGHT - GAP_HEIGHT - 100)

        # Top and bottom obstacle rectangles
        hitbox_padding_x = 16  # pixels to shrink on each side (left & right)
        hitbox_padding_y = 30  # optional, only if baguette is forgiving vertically

        # Create tighter baguette hitboxes
        top_rect = pygame.Rect(
            WIDTH + hitbox_padding_x,
            gap_y - OBSTACLE_HEIGHT + hitbox_padding_y,
            OBSTACLE_WIDTH - 2 * hitbox_padding_x,
            OBSTACLE_HEIGHT - hitbox_padding_y
        )

        bottom_rect = pygame.Rect(
            WIDTH + hitbox_padding_x,
            gap_y + GAP_HEIGHT,
            OBSTACLE_WIDTH - 2 * hitbox_padding_x,
            OBSTACLE_HEIGHT - hitbox_padding_y
        )


        obstacles.append({'rect': top_rect, 'kind': 'top', 'scored': False})
        obstacles.append({'rect': bottom_rect, 'kind': 'bottom', 'scored': False})


    # Move and draw obstacles
    for obstacle in obstacles:
        rect = obstacle['rect']
        kind = obstacle['kind']
        rect.x -= OBSTACLE_SPEED

        if kind == 'top':
            screen.blit(baguette_img_top, rect.topleft)
        else:
            screen.blit(baguette_img, rect.topleft)

        # Draw obstacle hitbox (DEBUG)
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)

    # Remove obstacles that go off-screen
    obstacles = [obs for obs in obstacles if obs['rect'].right > 0]

    # Apply gravity
    pigeon_velocity += GRAVITY
    pigeon_y += pigeon_velocity

    # Clamp to screen bounds (optional for now)
    if pigeon_y < 0:
        pigeon_y = 0
    if pigeon_y > HEIGHT - 128:
        pigeon_y = HEIGHT - 128



    # Animate pigeon
    pigeon_anim_timer += clock.get_time()
    if pigeon_anim_timer >= PIGEON_ANIM_SPEED:
        pigeon_anim_timer = 0
        pigeon_index = (pigeon_index + 1) % len(pigeon_frames)

    # Get current frame
    pigeon_frame = pigeon_frames[pigeon_index]

    # Draw the pigeon
    screen.blit(pigeon_frame, (pigeon_x, pigeon_y))

    # Pigeon hitbox
    pigeon_rect = pygame.Rect(pigeon_x + 32, pigeon_y + 26, 64, 76)

    # Draw pigeon hitbox (DEBUG)
    pygame.draw.rect(screen, (255, 0, 0), pigeon_rect, 2)  # Red outline


    # Check for collision
    for obstacle in obstacles:
        if pigeon_rect.colliderect(obstacle['rect']):
            print("💀 Collision! Pigeon hit a baguette!")
            running = False

    # Increment score when pigeon passes the middle of an obstacle pair
    for obstacle in obstacles:
        rect = obstacle['rect']
        kind = obstacle['kind']
        if kind == 'top' and rect.x + rect.width < pigeon_x and not obstacle['scored']:
            obstacle['scored'] = True
            score += 1

    # Render score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_text = font.render(f"Best: {high_score}", True, (255, 255, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_text, (10, 40))


    # Update the screen
    pygame.display.update()

    # Save high score
    if score > high_score:
        with open("highscore.txt", "w") as file:
            file.write(str(score))


# Quit Pygame cleanly
pygame.quit()
sys.exit()