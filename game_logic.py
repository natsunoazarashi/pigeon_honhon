import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 512
FPS = 60
OBSTACLE_WIDTH = 119
OBSTACLE_HEIGHT = 512
GAP_HEIGHT = 240
SPAWN_INTERVAL = 1500
OBSTACLE_SPEED = 3
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIGEON_ANIM_SPEED = 100


def load_scaled(path, size=(WIDTH, HEIGHT)):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)


def run_game(screen, clock, font, high_score):
    # Load assets
    bg_layers = {
        "sky": load_scaled("assets/background/sky.png"),
        "city": load_scaled("assets/background/city.png"),
        "quais": load_scaled("assets/background/quais.png"),
    }
    scroll_speeds = {"sky": 0.2, "city": 0.5, "quais": 1.0}

    baguette_img = pygame.image.load("assets/obstacles/baguette.png").convert_alpha()
    baguette_img_top = pygame.transform.flip(baguette_img, False, True)

    pigeon_sheet = pygame.image.load("assets/pigeon/pigeon_tileset.png").convert_alpha()
    pigeon_frames = [pigeon_sheet.subsurface(pygame.Rect(i * 128, 0, 128, 128)) for i in range(6)]

    # Load sounds
    flap_sound = pygame.mixer.Sound("assets/sounds/flap.wav")
    pass_sound = pygame.mixer.Sound("assets/sounds/obstacle_passed.wav")
    flap_sound.set_volume(0.6)
    pass_sound.set_volume(0.8)

    # Play background music
    pygame.mixer.music.load("assets/sounds/main_music.wav")
    pygame.mixer.music.set_volume(0.3)  # Volume between 0.0 et 1.0
    pygame.mixer.music.play(-1)  # -1 = infinite loop

    # Game variables
    scroll_x = 0
    pigeon_index = 0
    pigeon_anim_timer = 0
    pigeon_velocity = 0
    pigeon_x = 200
    pigeon_y = HEIGHT // 2
    score = 0

    obstacles = []
    last_spawn_time = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pigeon_velocity = JUMP_STRENGTH
                flap_sound.play() # we play the sound of flapping here because we press space!

        scroll_x += 2
        for layer_name in ["sky", "city", "quais"]:
            layer = bg_layers[layer_name]
            speed = scroll_speeds[layer_name]
            rel_x = -(scroll_x * speed) % layer.get_width()
            screen.blit(layer, (rel_x, 0))
            screen.blit(layer, (rel_x - layer.get_width(), 0))

        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > SPAWN_INTERVAL:
            last_spawn_time = current_time
            gap_y = random.randint(100, HEIGHT - GAP_HEIGHT - 100)
            hitbox_padding_x = 16
            hitbox_padding_y = 30
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

        for obstacle in obstacles:
            rect = obstacle['rect']
            kind = obstacle['kind']
            rect.x -= OBSTACLE_SPEED
            screen.blit(baguette_img_top if kind == 'top' else baguette_img, rect.topleft)
            # pygame.draw.rect(screen, (255, 0, 0), rect, 2)  # Debug

        obstacles = [obs for obs in obstacles if obs['rect'].right > 0]

        pigeon_velocity += GRAVITY
        pigeon_y += pigeon_velocity
        pigeon_y = max(0, min(pigeon_y, HEIGHT - 128))

        pigeon_anim_timer += clock.get_time()
        if pigeon_anim_timer >= PIGEON_ANIM_SPEED:
            pigeon_anim_timer = 0
            pigeon_index = (pigeon_index + 1) % len(pigeon_frames)

        pigeon_frame = pigeon_frames[pigeon_index]
        screen.blit(pigeon_frame, (pigeon_x, pigeon_y))

        pigeon_rect = pygame.Rect(pigeon_x + 32, pigeon_y + 26, 64, 76)
        # pygame.draw.rect(screen, (255, 0, 0), pigeon_rect, 2)  # Debug

        for obstacle in obstacles:
            if pigeon_rect.colliderect(obstacle['rect']):
                return score
                pygame.mixer.music.stop()

        for obstacle in obstacles:
            rect = obstacle['rect']
            kind = obstacle['kind']
            if kind == 'top' and rect.x + rect.width < pigeon_x and not obstacle['scored']:
                obstacle['scored'] = True
                score += 1
                pass_sound.play() # we passed the baguette, we play the sound

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_text = font.render(f"Best: {high_score}", True, (255, 255, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(high_text, (10, 40))

        pygame.display.update()

    return score
