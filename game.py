# https://www.youtube.com/watch?v=-8n91btt5d8
# Bugs:
# * blocks appear to move up a couple pixels while falling.
#   idk what could be causing this
#
# Improvement ideas:
# * Make it so that enemies only spawn in increments so that
#   impossible gaps will not occur
# * Difficulty modes
#   - settings file?
#   - mode where it doesn't speed up? easiest mode
# * Pause menu?
# * Leader board?
# * Hole in the wall game-mode

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
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = BLACK

# player variables
player_size = 50
player_pos = [WIDTH / 2, HEIGHT - 2 * player_size]
score = 0

# enemy variables
enemy_size = 50
enemy_pos = [0, 0]
enemy_speed = 5
NUM_ENEMIES = 25
enemy_list = [enemy_pos]
enemy_drop_range = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # The function accepts a tuple as the argument
game_over = False

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)


def set_level():
    speed = enemy_speed
    player_score = score
    if score % 20 == 0 and score != 0:
        speed += 1
        player_score += 1  # prevents rapid increase of speed
        # it makes sense from a game standpoint, as the player
        # is given an extra point for passing a milestone
    return speed, player_score


def drop_enemies(enemy_list):
    if len(enemy_list) < NUM_ENEMIES:
        # The following enemy spawns will cause random y's, but
        # they should be in line with the player's x's
        x_pos = 1

        while x_pos % 50 != 0:
            x_pos = random.randint(0, WIDTH - enemy_size)

        y_pos = random.randint(-enemy_size * enemy_drop_range, 0)

        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:  # Each element of the list is a list and is stepped through as "enemy"
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if -enemy_size * enemy_drop_range <= enemy_pos[1] <= HEIGHT:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1

    return score
    # if detect_collision(player_pos, enemy_pos):
    #     game_over = True
    #     break  # breaking the while loop here helps to stop block overlap by preventing the next draw
    #     # I'm not sure if the break still works if it is inside of a function


def collision_check(player_pos, enemy_list):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    # if the x values for the enemy fall between the x values for the player
    if (p_x <= e_x < p_x + player_size) or (p_x < e_x + enemy_size <= p_x + player_size):
        # if the x values overlap, the y values are checked
        if (p_y < e_y < p_y + player_size) or (p_y < e_y + enemy_size < p_y + player_size):
            # if both the x and y values overlap, collision occurs
            return True

    return False  # Only returns false if both if statements are not satisfied


# Beginning of game
# -----------------------------------------------------------------------
while not game_over:

    # It seems that anything regarding user events goes inside the following loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # Allows to exit out of the game with the
            sys.exit()  # x in the top right

        if event.type == pygame.KEYDOWN:

            # if player presses escape, game ends
            if event.key == pygame.K_ESCAPE:
                sys.exit()

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

    # Draw it
    screen.fill(BACKGROUND_COLOR)

    drop_enemies(enemy_list)
    draw_enemies(enemy_list)
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    enemy_speed, score = set_level()
    score = update_enemy_positions(enemy_list, score)
    # Score really doesnt need to be passed to the function because it
    # is not really updated until score is assigned the return value

    # The following variables are used with the score tracker
    text = "Score:" + str(score)
    label = myFont.render(text, 1, YELLOW)
    # MIT dude said that he thinks the 1 above means horizontal
    # and that if it was 0 the text would be vertical

    # Score tracker drawn on screen
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))

    if collision_check(player_pos, enemy_list):
        game_over = True
        print("Game Over")
        print("Final Score: " + str(score))

    clock.tick(FPS)

    pygame.display.update()
