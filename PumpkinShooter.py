import pygame
import random
import math

pygame.init()

# Creating Game Window
screen = pygame.display.set_mode((960, 600))
# Title and Icon
title = "Pumpkin Shooter"
icon = pygame.image.load('data/logo.png')
pygame.display.set_caption(title)
pygame.display.set_icon(icon)
# Background
bg = pygame.image.load('data/background.jpg')
pygame.mixer.music.load('data/bg_music.wav')
pygame.mixer.music.play(-1)
bullet_sound = pygame.mixer.Sound('data/laser.wav')
explosion_sound = pygame.mixer.Sound('data/explosion.wav')
# Player
player_img = pygame.image.load('data/player.png')
playerX = 448
playerY = 516
playerX_change = 0


def player(X, Y):
    screen.blit(player_img, (X, Y))


# enemy
num_of_enemies = 6
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('data/enemy.png'))
    enemyX.append(random.randint(0, 896))
    enemyY.append(random.randint(20, 120))
    enemyX_change.append(0.5)
    enemyY_change.append(40)


def enemy(X, Y, i):
    screen.blit(enemy_img[i], (X, Y))


# Bullets
bullet_img = pygame.image.load('data/bullet.png')
bulletX = 0
bulletY = 516
bulletY_change = -1
bullet_state = 'ready'
score = 0
score_font = pygame.font.Font('data/Aldrich-Regular.ttf', 32)
scoreX = 10
scoreY = 10

game_over_font = pygame.font.Font('data/Aldrich-Regular.ttf', 64)
game_overX = 300
game_overY = 200


def show_game_over(X, Y):
    global game_status
    game_over_img = game_over_font.render('Game Over', True, (255, 0, 0))
    screen.blit(game_over_img, (X, Y))
    pygame.mixer.music.stop()
    game_status = 'end'


restart_font = pygame.font.Font('data/Aldrich-Regular.ttf', 32)
restartX = 320
restartY = 330
game_status = 'running'


def show_restart(X, Y):
    restart_img = restart_font.render('Press R to restart', True, (0, 255, 0))
    screen.blit(restart_img, (X, Y))


def show_score(X, Y):
    score_img = score_font.render('Score:' + str(score), True, (255, 255, 255))
    screen.blit(score_img, (X, Y))


def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
    if distance < 25:
        return True
    else:
        return False


def bullet(X, Y):
    screen.blit(bullet_img, (X + 16, Y + 10))


game_on = True
while game_on:
    # Background RGB
    screen.fill((45, 51, 71))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.7
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_state = 'fire'
                    bulletX = playerX
                    bullet(bulletX, bulletY)
                    bullet_sound.play()
            if event.key == pygame.K_r:
                if game_status == 'end':
                    game_status = 'running'
                    score = 0
                    playerX = 448
                    pygame.mixer.music.play(-1)
                    for i in range(num_of_enemies):
                        enemyX[i] = random.randint(0, 896)
                        enemyY[i] = random.randint(20, 120)
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # Bullet Moments
    if bullet_state == 'fire':
        if bulletY < 10:
            bulletY = 516
            bullet_state = 'ready'
        bulletY += bulletY_change
        bullet(bulletX, bulletY)
    # Enemy Moments
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 466:
            show_restart(restartX, restartY)
            show_game_over(game_overX, game_overY)
            for j in range(num_of_enemies):
                enemyY[j] = 1200
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 896:
            enemyX[i] = 896
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]
        enemy(enemyX[i], enemyY[i], i)
        # collision Moments
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 516
            bullet_state = 'ready'
            enemyX[i] = random.randint(0, 896)
            enemyY[i] = random.randint(20, 120)
            score += 1
            explosion_sound.play()
    show_score(scoreX, scoreY)
    # Player Moments
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 896:
        playerX = 896
    player(playerX, playerY)

    pygame.display.update()
