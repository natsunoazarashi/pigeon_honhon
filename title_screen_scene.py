import pygame
import os

# Const
WIDTH, HEIGHT = 800, 512
CLOUD_SCROLL_SPEED = 0.2

# assets loading
def load_assets():
    base_path = "assets/background"

    sky = pygame.image.load(os.path.join(base_path, "background_sky.png")).convert()

    clouds_raw = pygame.image.load(os.path.join(base_path, "tileset_clouds.png")).convert_alpha()
    clouds = pygame.transform.scale_by(clouds_raw, 0.5)

    eiffel_raw = pygame.image.load(os.path.join(base_path, "title_screen_eiffel_tower.png")).convert_alpha()
    eiffel = pygame.transform.scale_by(eiffel_raw, 0.5)

    foreground = pygame.image.load(os.path.join(base_path, "title_screen_foreground.png")).convert_alpha()

    return sky, clouds, eiffel, foreground


# displays title screen with effects
class TitleScreen:
    def __init__(self):
        self.sky, self.clouds, self.eiffel, self.foreground = load_assets()
        self.cloud_x = 0
        self.title_font = pygame.font.Font(None, 72)  # uses freesansbold.ttf


    def update(self):
        self.cloud_x -= CLOUD_SCROLL_SPEED
        if self.cloud_x <= -self.clouds.get_width():
            self.cloud_x = 0

    def draw(self, screen):
        screen.blit(self.sky, (0, 0))  # Sky in the back

        y_clouds = -30
        screen.blit(self.clouds, (self.cloud_x, y_clouds))
        screen.blit(self.clouds, (self.cloud_x + self.clouds.get_width(), y_clouds))

        eiffel_x = WIDTH - self.eiffel.get_width() - 100  # move 100px left
        eiffel_y = 260 - self.eiffel.get_height() + 25    # move 25px down # manually aligned to background "ground"
        eiffel_y = max(0, eiffel_y)  # ensures the tower is not drawn offscreen
        # TEMP: draw a red rectangle where the Eiffel Tower should be
        screen.blit(self.eiffel, (eiffel_x, eiffel_y))

        screen.blit(self.foreground, (0, 0))  # Foreground: bench, pigeon, text

        # Title

        # Shadow effect
        shadow = self.title_font.render("Pigeon Hon Hon", True, (0, 0, 0))
        screen.blit(shadow, (WIDTH // 2 - shadow.get_width() // 2 + 3, 43))

        # Main title
        title = self.title_font.render("Pigeon Hon Hon", True, (255, 255, 0))  # bright yellow
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))


