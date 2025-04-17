import pygame
import os

# Const
WIDTH, HEIGHT = 800, 512
FRAME_WIDTH = 256
FRAME_HEIGHT = 256
FPS = 6  # frame rate animation (~6 fps)

class GameOverScene:
    def __init__(self):
        # background loading
        self.background = pygame.image.load(os.path.join("assets", "background", "game_over_background.png")).convert()

        # tileset loading and frames extraction
        tileset_path = os.path.join("assets", "background", "pigeon_game_over_tileset.png")
        tileset = pygame.image.load(tileset_path).convert_alpha()
        self.frames = [tileset.subsurface(pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
                       for i in range(tileset.get_width() // FRAME_WIDTH)]

    def play(self, screen):
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        frame_index = 0
        num_frames = len(self.frames)

        # Durée animation normale (5 sec)
        animation_duration = 5000
        fade_duration = 1000  # 1 seconde de fade

        fade_started = False
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))

        while True:
            elapsed = pygame.time.get_ticks() - start_time

            # Fin totale après animation + fade
            if elapsed > animation_duration + fade_duration:
                break

            screen.blit(self.background, (0, 0))

            # Animation pigeon
            if elapsed < animation_duration:
                frame = self.frames[frame_index]
                screen.blit(frame, (
                    WIDTH // 2 - FRAME_WIDTH // 2,
                    HEIGHT // 2 - FRAME_HEIGHT // 2
                ))
                frame_index = (frame_index + 1) % num_frames

            # Début du fade après les 5 sec
            if elapsed > animation_duration:
                fade_alpha = int(((elapsed - animation_duration) / fade_duration) * 255)
                fade_alpha = min(fade_alpha, 255)
                fade_surface.set_alpha(fade_alpha)
                screen.blit(fade_surface, (0, 0))

            pygame.display.update()
            clock.tick(FPS)


