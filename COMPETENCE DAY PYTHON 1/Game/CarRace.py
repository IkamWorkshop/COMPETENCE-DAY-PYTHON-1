import pygame
import random
import sys
import os

# Inisialisasi pygame
pygame.init()

# Ukuran layar
WIDTH = 800  # Diperbesar dari 400 ke 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing - Map Besar")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)

# Load gambar (fallback jika tidak ada)
def create_car_image(color, width=60, height=100):
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.fill(color)
    # Body mobil
    pygame.draw.rect(image, color, (10, 0, width-20, height-20))
    # Jendela
    pygame.draw.rect(image, BLACK, (15, 15, width-30, 30))
    # Lampu
    pygame.draw.rect(image, YELLOW, (10, 5, 10, 10))
    pygame.draw.rect(image, YELLOW, (width-20, 5, 10, 10))
    return image

# Buat gambar mobil
player_img = create_car_image((0, 0, 255))  # Mobil biru
enemy_img = create_car_image((255, 0, 0))   # Mobil merah

# Gambar jalan raya
road_width = 600  # Lebar jalan diperbesar
road_x = (WIDTH - road_width) // 2
road_img = pygame.Surface((road_width, HEIGHT))
road_img.fill(GRAY)
# Marka jalan tengah
for i in range(0, HEIGHT, 40):
    pygame.draw.rect(road_img, WHITE, (road_width//2 - 25, i, 50, 20))

# Pemain
player_width = 60
player_height = 100
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20
player_speed = 50  # Kecepatan sedikit dinaikkan

# Musuh (mobil lawan)
enemies = []
enemy_speed = 10  # Kecepatan musuh dikurangi
enemy_frequency = 50  # Frekuensi muncul musuh dikurangi (semakin besar semakin jarang)
enemy_width = 60
enemy_height = 100

# Skor
score = 0
font = pygame.font.SysFont('Arial', 36)

clock = pygame.time.Clock()

def draw_environment():
    # Gambar latar belakang
    screen.fill(GREEN)  # Rumput
    screen.blit(road_img, (road_x, 0))  # Jalan

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def create_enemy():
    # Buat musuh di salah satu dari 3 jalur
    lanes = [road_x + road_width//4 - enemy_width//2,
             road_x + road_width//2 - enemy_width//2,
             road_x + 3*road_width//4 - enemy_width//2]
    x = random.choice(lanes)
    enemies.append([x, -enemy_height])

def draw_enemies():
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))

def update_enemies():
    global score
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)
            score += 1

def check_collision():
    for enemy in enemies:
        if (player_y < enemy[1] + enemy_height and
            player_y + player_height > enemy[1] and
            player_x < enemy[0] + enemy_width and
            player_x + player_width > enemy[0]):
            return True
    return False

# Game loop utama
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Gerakan pemain
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > road_x + 20:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < road_x + road_width - player_width - 20:
        player_x += player_speed
    
    # Buat musuh baru (dikurangi frekuensinya)
    if random.randint(1, enemy_frequency) == 1:
        create_enemy()
    
    # Update musuh
    update_enemies()
    
    # Cek tabrakan
    if check_collision():
        running = False
    
    # Gambar semua elemen
    draw_environment()
    draw_player(player_x, player_y)
    draw_enemies()
    
    # Tampilkan skor
    score_text = font.render(f"Skor: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))
    
    pygame.display.update()
    clock.tick(60)

# Layar game over
screen.fill(WHITE)
game_over_text = font.render(f"Game Over! Skor: {score}", True, BLACK)
restart_text = font.render("Tekan R untuk restart, Q untuk keluar", True, BLACK)
screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 10))
pygame.display.update()

# Tunggu input player
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                os.execv(sys.executable, ['python'] + sys.argv)
            if event.key == pygame.K_q:
                waiting = False

pygame.quit()
sys.exit()