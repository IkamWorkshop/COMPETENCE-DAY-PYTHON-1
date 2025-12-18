import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()
pygame.mixer.init()

# Setup Layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Invaders Emoji Edition")

# Warna
BLACK = (0, 0, 20)
PURPLE = (100, 0, 150)
BLUE = (0, 100, 255)
WHITE = (255, 255, 255)

# Asset Emoji (ganti dengan font yang support emoji)
font_emoji = pygame.font.SysFont("segoeuiemoji", 40)

# Player
player_emoji = "🚀"
player_x = WIDTH // 2
player_speed = 5
player_bullets = []

# Musuh
enemies = []
for _ in range(8):
    enemies.append({
        "emoji": random.choice(["👾", "🤖", "👽", "🛸"]),
        "x": random.randint(50, WIDTH-50),
        "y": random.randint(50, 200),
        "speed": random.choice([1, -1]) * 2
    })

# Efek Partikel
particles = []

# Skor
score = 0
font_score = pygame.font.SysFont("Arial", 30)

def draw_player():
    text = font_emoji.render(player_emoji, True, WHITE)
    screen.blit(text, (player_x - 20, HEIGHT - 60))

def draw_enemies():
    for enemy in enemies:
        text = font_emoji.render(enemy["emoji"], True, (255, 50, 50))
        screen.blit(text, (enemy["x"], enemy["y"]))

def draw_bullets():
    for bullet in player_bullets:
        pygame.draw.rect(screen, BLUE, (bullet["x"], bullet["y"], 5, 15))

def create_particles(x, y):
    for _ in range(20):
        particles.append({
            "x": x,
            "y": y,
            "color": random.choice([(255, 50, 50), (255, 150, 50), (100, 255, 255)]),
            "size": random.randint(3, 8),
            "speed_x": random.uniform(-3, 3),
            "speed_y": random.uniform(-3, 3),
            "life": 30
        })

def draw_particles():
    for p in particles[:]:
        pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), p["size"])
        p["x"] += p["speed_x"]
        p["y"] += p["speed_y"]
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)

def show_score():
    score_text = font_score.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Game Loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)
    
    # Background stars
    for _ in range(2):
        pygame.draw.circle(screen, WHITE, 
                         (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 
                         1)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_bullets.append({"x": player_x, "y": HEIGHT - 80})
    
    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 30:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 30:
        player_x += player_speed
    
    # Enemy Movement
    for enemy in enemies[:]:
        enemy["x"] += enemy["speed"]
        if enemy["x"] <= 0 or enemy["x"] >= WIDTH - 40:
            enemy["speed"] *= -1
            enemy["y"] += 40
        
        # Collision Bullet-Enemy
        for bullet in player_bullets[:]:
            if (enemy["x"] < bullet["x"] < enemy["x"] + 40 and
                enemy["y"] < bullet["y"] < enemy["y"] + 40):
                create_particles(enemy["x"], enemy["y"])
                enemies.remove(enemy)
                player_bullets.remove(bullet)
                score += 10
                break
    
    # Bullet Movement
    for bullet in player_bullets[:]:
        bullet["y"] -= 7
        if bullet["y"] < 0:
            player_bullets.remove(bullet)
    
    # Drawing
    draw_enemies()
    draw_player()
    draw_bullets()
    draw_particles()
    show_score()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()