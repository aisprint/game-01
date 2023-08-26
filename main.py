import pygame
import random

# 初期化
pygame.init()

# 色の設定
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 画面のサイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# ブロックのサイズ
BLOCK_WIDTH = 80
BLOCK_HEIGHT = 30

# ボールのサイズ
BALL_RADIUS = 7.5

# パドルのサイズ
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20

# 画面設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('ブロック崩し')

# パドルとボールの初期位置
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
ball_x = random.randint(0, SCREEN_WIDTH)
ball_y = SCREEN_HEIGHT // 2
ball_dx = random.choice([-1, 1])
ball_dy = -1

# ブロックの配置
blocks = []
for i in range(5):
    for j in range(10):
        block_x = j * (BLOCK_WIDTH + 10)
        block_y = i * (BLOCK_HEIGHT + 10)
        blocks.append(pygame.Rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT))

game_over = False
win = False
running = True

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= 5
    if keys[pygame.K_RIGHT]:
        paddle_x += 5

    paddle_x = max(0, min(SCREEN_WIDTH - PADDLE_WIDTH, paddle_x))
    
    pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    ball_x += ball_dx * 5
    ball_y += ball_dy * 5

    if ball_x < 0 or ball_x > SCREEN_WIDTH:
        ball_dx = -ball_dx

    if ball_y < 0:
        ball_dy = -ball_dy

    # ボールが画面の下端に到達
    if ball_y > SCREEN_HEIGHT:
        game_over = True
        running = False  # ゲーム終了

    if (paddle_x < ball_x < paddle_x + PADDLE_WIDTH) and (paddle_y < ball_y < paddle_y + PADDLE_HEIGHT):
        ball_dy = -ball_dy

    hit_blocks = []
    for block in blocks:
        if block.collidepoint(ball_x, ball_y):
            ball_dy = -ball_dy
            hit_blocks.append(block)

    for block in hit_blocks:
        blocks.remove(block)

    # 勝利条件: すべてのブロックが消えた場合
    if len(blocks) == 0:
        win = True
        running = False  # ゲーム終了

    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), int(BALL_RADIUS))

    for block in blocks:
        pygame.draw.rect(screen, BLUE, block)

    pygame.display.flip()
    pygame.time.wait(10)

# ゲームが終了した後のメッセージ表示
if game_over:
    print("ゲームオーバー！")
elif win:
    print("勝利！")

pygame.quit()
