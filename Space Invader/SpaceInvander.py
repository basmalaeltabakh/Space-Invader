import math
import random
import pygame
from pygame import mixer

# تهيئة Pygame
pygame.init()

# إعداد الشاشة
screen = pygame.display.set_mode((800, 600))

# تحميل الخلفية
background = pygame.image.load('background.jpg')

# تشغيل الصوت
mixer.music.load("background.wav")
mixer.music.play(-1)

# إعداد الأيقونة والعنوان
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('shuttle.png')
pygame.display.set_icon(icon)

# اللاعب
playerImg = pygame.image.load('space.png')
playerX = 370
playerY = 480
player_speed = 0  
acceleration = 0.2  
max_speed = 5  
friction = 0.1  

# الأعداء
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('game.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)  
    enemyY_change.append(10)   

# الرصاصة
bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (10, 20))  
bulletX = 0
bulletY = playerY  
bulletY_change = 10  
bullet_state = "ready"  

# إعداد الخطوط والنقاط
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# نص نهاية اللعبة والفوز
over_font = pygame.font.Font('freesansbold.ttf', 64)
win_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    global score_value
    if score_value >= 30:
        win_text = win_font.render("YOU WIN!", True, (0, 255, 0))
        screen.blit(win_text, (250, 250))
    else:
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y - 20))  

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    return distance < 27

# 🔥 حلقة اللعبة الرئيسية
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # التقاط الأحداث
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # إطلاق الرصاصة عند الضغط على المسافة
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if bullet_state == "ready":
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

    # قراءة المفاتيح لتحريك اللاعب
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_speed -= acceleration  
    elif keys[pygame.K_RIGHT]:
        player_speed += acceleration  
    else:
        if player_speed > 0:
            player_speed -= friction  
        elif player_speed < 0:
            player_speed += friction  

    # منع تجاوز السرعة القصوى
    player_speed = max(-max_speed, min(player_speed, max_speed))

    # تحريك اللاعب
    playerX += player_speed
    playerX = max(0, min(playerX, 736))  

    # إذا وصل اللاعب إلى 30 نقطة، يتم إيقاف الأعداء وعرض رسالة الفوز
    if score_value < 30:
        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.5  
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.5  
                enemyY[i] += enemyY_change[i]

            # التحقق من التصادم
            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bulletY = playerY  
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

    # تحريك الرصاصة
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change  
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"  

    # عرض اللاعب والنقاط
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
