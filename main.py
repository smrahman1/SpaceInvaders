import random
import math
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create Screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("Background.jpg")
mixer.music.load("backgroundMusic.mp3")
mixer.music.set_volume(0.025)
mixer.music.play(-1)
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Icon.png")
pygame.display.set_icon(icon)

# Scoreboard
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

overFont = pygame.font.Font("freesansbold.ttf", 50)


def scoreboard():
    scoreboard = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(scoreboard, (10, 10))


# Spaceship
playerImg = pygame.image.load("Spaceship.png")
playerX = 370
playerY = 520
playerChange = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyNum = 6

for i in range(enemyNum):
    enemyImg.append(pygame.image.load("Enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(0.5)
    enemyYChange = 64

# Bullet
bulletImg = pygame.image.load("Bullet.png")
bulletX = 0
bulletY = 480
bulletChange = 1
bulletState = "Ready"


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet_fire(x, y):
    global bulletState
    bulletState = "Fire"
    screen.blit(bulletImg, (x + 15, y + 10))


def checkCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 30:
        explosion = mixer.Sound("collisionSound.mp3")
        explosion.set_volume(0.3)
        explosion.play()
        return True
    return False


def gameOver():
    gameOverText = overFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameOverText, (260, 240))


# Show Screen Loop
running = True

while running:
    # Background colour
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                playerChange = -0.7
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                playerChange = 0.7
            if event.key == pygame.K_SPACE:
                if bulletState == "Ready":
                    bulletX = playerX
                    bulletSound = mixer.Sound("bulletSound.mp3")
                    bulletSound.set_volume(0.035)
                    bulletSound.play()
                bullet_fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerChange = 0
    playerX += playerChange
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    for i in range(enemyNum):

        # Check Game Over
        if enemyY[i] > 440:
            for j in range(enemyNum):
                enemyY[j] = 2000
            gameOver()
            mixer.music.stop()
            break

        enemyX[i] += enemyXChange[i]
        if enemyX[i] > 736:
            enemyXChange[i] = -0.5
            enemyY[i] += enemyYChange
        elif enemyX[i] < 0:
            enemyXChange[i] = 0.5
            enemyY[i] += enemyYChange

        collision = checkCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bulletState = "Ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            randnum = random.randint(0, 100)
            if randnum > 50:
                enemyXChange[i] = 0.5
            else:
                enemyXChange[i] = -0.5
        enemy(enemyX[i], enemyY[i], i)
    if bulletY < -5:
        bulletY = 500
        bulletState = "Ready"
    if bulletState == "Fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletChange

    player(playerX, playerY)
    scoreboard()
    pygame.display.update()
