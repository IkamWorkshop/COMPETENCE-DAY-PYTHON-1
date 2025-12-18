import pygame
import random
import sys
import math

# Inisialisasi Pygame
pygame.init()

# Konfigurasi Layar
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Realistis")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Variabel Game
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
font = pygame.font.SysFont('Arial', 30, bold=True)
flap_angle = 0
flap_direction = 1

# Fungsi menggambar burung
def draw_bird(x, y):
    # Badan burung (elips kuning)
    pygame.draw.ellipse(screen, YELLOW, (x, y, 40, 30))
    
    # Mata
    pygame.draw.circle(screen, BLACK, (x + 30, y + 10), 4)
    
    # Paruh (segitiga)
    pygame.draw.polygon(screen, RED, [(x + 40, y + 15), 
                                     (x + 50, y + 15), 
                                     (x + 40, y + 20)])
    
    # Sayap (bergerak naik turun)
    global flap_angle, flap_direction
    flap_angle += 0.2 * flap_direction
    if abs(flap_angle) > 0.5:
        flap_direction *= -1
    
    wing_y = y + 15 + 5 * math.sin(flap_angle)
    pygame.draw.ellipse(screen, YELLOW, (x - 10, wing_y, 30, 15))

# Fungsi membuat pipa dengan tekstur
def draw_pipe(x, y, height, is_top=False):
    # Warna dasar pipa
    pipe_color = DARK_GREEN
    
    # Gambar pipa utama
    pygame.draw.rect(screen, pipe_color, (x, y, 60, height))
    
    # Tambahkan detail garis-garis pada pipa
    for i in range(0, height, 20):
        pygame.draw.rect(screen, GREEN, (x, y + i, 60, 10))
    
    # Tambahkan pinggiran pipa
    edge_width = 5
    pygame.draw.rect(screen, (50, 50, 50), (x - edge_width, y, edge_width, height))
    
    # Jika pipa atas, balik secara vertikal
    if is_top:
        pygame.draw.rect(screen, pipe_color, (x, y, 60, 20))  # Tambahkan ujung pipa
        pygame.draw.rect(screen, (50, 50, 50), (x - edge_width, y, edge_width, 20))
    else:
        pygame.draw.rect(screen, pipe_color, (x, y + height - 20, 60, 20))  # Ujung pipa
        pygame.draw.rect(screen, (50, 50, 50), (x - edge_width, y + height - 20, edge_width, 20))

# Burung (Player)
bird_rect = pygame.Rect(100, HEIGHT // 2, 40, 30)

# Pipa (Rintangan)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)  # Muncul pipa setiap 1.5 detik

# Fungsi untuk membuat pipa baru
def create_pipe():
    random_pipe_pos = random.randint(200, 400)
    bottom_pipe_height = HEIGHT - random_pipe_pos
    top_pipe_height = random_pipe_pos - 150
    
    bottom_pipe = {
        'x': WIDTH,
        'y': random_pipe_pos,
        'height': bottom_pipe_height,
        'passed': False
    }
    
    top_pipe = {
        'x': WIDTH,
        'y': 0,
        'height': top_pipe_height,
        'passed': False
    }
    
    return bottom_pipe, top_pipe

# Fungsi untuk memindahkan pipa
def move_pipes(pipes):
    for pipe in pipes:
        pipe['x'] -= 3  # Kecepatan pipa bergerak ke kiri
    return [pipe for pipe in pipes if pipe['x'] + 60 > 0]

# Fungsi untuk deteksi tabrakan
def check_collision(pipes):
    for pipe in pipes:
        pipe_rect = pygame.Rect(pipe['x'], pipe['y'], 60, pipe['height'])
        if bird_rect.colliderect(pipe_rect):
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return False

    return True

# Fungsi untuk menampilkan skor
def display_score(game_state):
    if game_state == 'active':
        score_surface = font.render(f"Score: {int(score)}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, 50))
        screen.blit(score_surface, score_rect)
    else:
        # Tampilkan skor akhir
        score_surface = font.render(f"Score: {int(score)}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, 50))
        screen.blit(score_surface, score_rect)

        # Tampilkan high score
        high_score_surface = font.render(f"High Score: {int(high_score)}", True, WHITE)
        high_score_rect = high_score_surface.get_rect(center=(WIDTH // 2, 100))
        screen.blit(high_score_surface, high_score_rect)

        # Tampilkan instruksi
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(restart_text, restart_rect)

# Game Loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -7  # Burung melompat saat SPASI ditekan
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, HEIGHT // 2)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())

    # Background
    screen.fill(SKY_BLUE)

    if game_active:
        # Gerakan Burung
        bird_movement += gravity
        bird_rect.centery += bird_movement

        # Gambar Burung
        draw_bird(bird_rect.x, bird_rect.y)

        # Pipa
        pipe_list = move_pipes(pipe_list)
        for pipe in pipe_list:
            draw_pipe(pipe['x'], pipe['y'], pipe['height'], pipe['y'] == 0)
            
            # Cek jika burung melewati pipa
            if pipe['x'] + 60 < bird_rect.left and not pipe['passed']:
                pipe['passed'] = True
                score += 0.5  # Setiap pasang pipa (atas+bawah) bernilai 1 poin

        # Skor
        display_score('active')

        # Tabrakan
        game_active = check_collision(pipe_list)
    else:
        # Game Over Screen
        if score > high_score:
            high_score = score
        display_score('game_over')

    pygame.display.update()
    clock.tick(60)  # 60 FPS