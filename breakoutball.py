import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10

# Ball properties
BALL_RADIUS = 8
BALL_SPEED = 5

# Brick properties
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 30

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Ball Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Paddle class
class Paddle:
    def __init__(self):
        self.x = WIDTH // 2 - PADDLE_WIDTH // 2
        self.y = HEIGHT - 40
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        elif direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed

# Ball class
class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = BALL_RADIUS
        self.x_speed = BALL_SPEED * random.choice([-1, 1])
        self.y_speed = -BALL_SPEED

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed

        # Bounce off walls
        if self.x <= 0 or self.x >= WIDTH:
            self.x_speed *= -1
        if self.y <= 0:
            self.y_speed *= -1

    def check_collision(self, paddle):
        if (
            self.y + self.radius >= paddle.y
            and paddle.x <= self.x <= paddle.x + paddle.width
        ):
            self.y_speed *= -1

# Brick class
class Brick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.alive = True

    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

    def check_collision(self, ball):
        if (
            self.alive
            and self.x <= ball.x <= self.x + self.width
            and self.y <= ball.y <= self.y + self.height
        ):
            self.alive = False
            ball.y_speed *= -1
            return True
        return False

# Initialize objects
paddle = Paddle()
ball = Ball()
bricks = [
    Brick(col * BRICK_WIDTH, row * BRICK_HEIGHT)
    for row in range(BRICK_ROWS)
    for col in range(BRICK_COLS)
]

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move("left")
    if keys[pygame.K_RIGHT]:
        paddle.move("right")

    # Ball movement
    ball.move()
    ball.check_collision(paddle)

    # Check collisions with bricks
    for brick in bricks:
        brick.check_collision(ball)

    # Draw everything
    paddle.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()

    # Game over
    if ball.y > HEIGHT:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Win condition
    if all(not brick.alive for brick in bricks):
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()