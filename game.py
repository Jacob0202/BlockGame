# https://www.youtube.com/watch?v=-8n91btt5d8

import pygame
import sys
import random

pygame.init()

# window and game settings
WIDTH = 800
HEIGHT = 600
FPS = 30

# color variables
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = BLACK

# player variables
player_size = 50
player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]

# enemy variables
enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
ENEMY_SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # The function accepts a tuple as the argument
game_over = False

clock = pygame.time.Clock()


def detect_collsions(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    # if the x values for the enemy fall between the x values for the player
    if (p_x < e_x < p_x + player_size) or (p_x < e_x + enemy_size < p_x + player_size):
        # if the x values overlap, the y values are checked
        if (p_y < e_y < p_y + player_size) or (p_y < e_y + enemy_size < p_y + player_size):
            # if both the x and y values overlap, collison occurs
            return True

    return False  # Only returns false if both if statements are not satisfied


# Beginning of game
# ------------------
while not game_over:

    # It seems that anything regarding user events goes inside the following loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # Allows to exit out of the game with the
            sys.exit()  # x in the top right

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]

            # changes player position within bounds
            if event.key == pygame.K_LEFT and x != 0:
                x -= player_size
            elif event.key == pygame.K_RIGHT and x != WIDTH - player_size:
                x += player_size
            elif event.key == pygame.K_DOWN and y != HEIGHT - player_size:
                y += player_size
            elif event.key == pygame.K_UP and y != 0:
                y -= player_size

            # update player_pos list
            player_pos = [x, y]

    # Update enemy position
    if enemy_pos[1] >= 0 and enemy_pos[1] <= HEIGHT:
        enemy_pos[1] += ENEMY_SPEED
    else:
        enemy_pos[0] = random.randint(0, WIDTH - enemy_size)
        enemy_pos[1] = 0

    if detect_collsions(player_pos, enemy_pos):
        game_over = True
        print("Game Over")
        break  # breaking the while loop here helps to stop block overlap by preventing the next draw

    # Draw it
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(FPS)

    pygame.display.update()
