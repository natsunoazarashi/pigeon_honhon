import pygame
import sys
import os
from game_logic import run_game  # importing game logic
from title_screen_scene import TitleScreen # importing title screen
from game_over_scene import GameOverScene # importing game over screen

pygame.init()

# global const
WIDTH, HEIGHT = 800, 512
FPS = 60



# screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pigeon Hon Hon")

# Load splash screen
# title_img = pygame.image.load("assets/background/title_screen.png").convert()

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)



# high score loading
high_score = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        try:
            high_score = int(file.read())
        except:
            high_score = 0

# game states : 'start', 'play', 'game_over'
game_state = 'start'
last_score = 0

running = True
title_screen = TitleScreen()
game_over_scene = GameOverScene()
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # If we are in a menu, we start with SPACE
        if game_state in ['start', 'game_over']:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = 'play'

    screen.fill((0, 0, 0))  # cleans screen

    if game_state == 'start':
        # screen.blit(title_img, (0, 0))  # 💡 Affiche le splash screen
        title_screen.update()
        title_screen.draw(screen)
        prompt = font.render("Press SPACE to start", True, (255, 255, 255))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT - 50))
        pygame.display.update()
        continue

    if game_state == 'game_over':
        game_over_text = font.render("💥 Game Over", True, (255, 80, 80))
        score_text = font.render(f"Score: {last_score}", True, (255, 255, 255))
        best_text = font.render(f"Best: {high_score}", True, (255, 255, 0))
        restart_text = font.render("Press SPACE to restart", True, (200, 200, 200))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, HEIGHT // 2 + 20))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))
        pygame.display.update()
        continue

    # If we are in-game → main function call
    if game_state == 'play':
        last_score = run_game(screen, clock, font, high_score)
        if last_score > high_score:
            high_score = last_score
            with open("highscore.txt", "w") as file:
                file.write(str(high_score))
        game_over_scene.play(screen)
        game_state = 'game_over'

pygame.quit()
sys.exit()
