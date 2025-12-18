import pygame
import random
import sys
import time

# Inisialisasi Pygame
pygame.init()

# Warna
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID_COLOR = (50, 50, 50)

# Pengaturan Game
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Efek Visual
PARTICLE_EFFECTS = []

# Setup Layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Premium")
clock = pygame.time.Clock()

# Load Font
font_large = pygame.font.SysFont('arial', 50, bold=True)
font_medium = pygame.font.SysFont('arial', 30)
font_small = pygame.font.SysFont('arial', 20)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1
        self.score = 0
        self.color = LIGHT_GREEN
        self.head_color = GOLD
        self.speed = FPS
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_head = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        
        if new_head in self.positions[1:]:
            return False  # Game over
            
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return True
    
    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1
        self.score = 0
    
    def render(self, surface):
        # Gambar ekor
        for i, p in enumerate(self.positions[1:]):
            pygame.draw.rect(surface, self.color, (p[0]*GRID_SIZE, p[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BLACK, (p[0]*GRID_SIZE, p[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
        
        # Gambar kepala (berbeda warna)
        head = self.get_head_position()
        pygame.draw.rect(surface, self.head_color, (head[0]*GRID_SIZE, head[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Mata ular
        eye_size = GRID_SIZE // 5
        dir_x, dir_y = self.direction
        
        # Mata mengikuti arah gerakan
        if dir_x == 1:  # Kanan
            pygame.draw.circle(surface, BLACK, (head[0]*GRID_SIZE + GRID_SIZE - eye_size, head[1]*GRID_SIZE + eye_size*2), eye_size)
            pygame.draw.circle(surface, BLACK, (head[0]*GRID_SIZE + GRID_SIZE - eye_size, head[1]*GRID_SIZE + GRID_SIZE - eye_size*2), eye_size)
        elif dir_x == -1:  # Kiri
            pygame.draw.circle(surface, BLACK, (head[0]*GRID_SIZE + eye_size, head[1]*GRID_SIZE + eye_size*2), eye_size)
            pygame.draw.circle(surface, BLACK, (head[0]*GRID_SIZE + eye_size, head[1]*GRID_SIZE + GRID_SIZE - eye_size*2), eye_size)
        elif dir_y == 1:  # Bawah
            pygame.draw.circle(surface, BLACK, (head[0]*GRID_SIZE + eye_size*2, head[1]*GRID_SIZE + GRID_SIZE - eye_size), eye_size)
            pygame.draw.circle(surface, BLACK, (head[0]*GRID_SIZE + GRID_SIZE - eye_size*2, head[1]*GRID_SIZE + GRID_SIZE - eye_size), eye_size)
        else:  # Atas
            pygame.draw.circle(surface, BLACK, (head[0]*GRID_SIZE + eye_size*2, head[1]*GRID_SIZE + eye_size), eye_size)
            pygame.draw.circle(surface, BLACK, (head[0]*GRID_SIZE + GRID_SIZE - eye_size*2, head[1]*GRID_SIZE + eye_size), eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
        self.sparkle_time = 0
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        
    def render(self, surface):
        # Efek berkelap-kelip
        self.sparkle_time += 1
        sparkle_factor = 0.8 + 0.2 * abs(math.sin(self.sparkle_time * 0.1))
        current_red = min(255, int(self.color[0] * sparkle_factor))
        
        # Gambar makanan dengan efek gradien
        center_x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        center_y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
        
        # Efek cahaya
        pygame.draw.circle(surface, (current_red, 50, 50), (center_x, center_y), GRID_SIZE // 2 + 2)
        pygame.draw.circle(surface, (current_red, 0, 0), (center_x, center_y), GRID_SIZE // 2)
        
        # Efek highlight
        pygame.draw.circle(surface, (255, 255, 255, 100), 
                          (center_x - GRID_SIZE//4, center_y - GRID_SIZE//4), 
                          GRID_SIZE//6)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)

def show_game_over(surface, score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    
    game_over_text = font_large.render("GAME OVER", True, WHITE)
    score_text = font_medium.render(f"Score: {score}", True, GOLD)
    restart_text = font_small.render("Press SPACE to restart", True, WHITE)
    
    surface.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
    surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

def main():
    snake = Snake()
    food = Food()
    game_over = False
    last_score = 0
    
    # Efek partikel
    particles = []
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    snake.reset()
                    food.randomize_position()
                    game_over = False
                elif not game_over:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
        
        if not game_over:
            # Update game state
            if not snake.update():
                game_over = True
                last_score = snake.score
            
            # Cek jika ular makan makanan
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                
                # Efek partikel
                for _ in range(20):
                    particles.append({
                        'x': food.position[0] * GRID_SIZE + GRID_SIZE//2,
                        'y': food.position[1] * GRID_SIZE + GRID_SIZE//2,
                        'dx': random.uniform(-2, 2),
                        'dy': random.uniform(-2, 2),
                        'life': 30,
                        'color': (random.randint(200, 255), random.randint(100, 200), 0)
                    })
                
                food.randomize_position()
                # Pastikan makanan tidak muncul di badan ular
                while food.position in snake.positions:
                    food.randomize_position()
        
        # Update partikel
        for p in particles[:]:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['life'] -= 1
            if p['life'] <= 0:
                particles.remove(p)
        
        # Gambar layar
        screen.fill(BLACK)
        draw_grid(screen)
        
        # Gambar partikel
        for p in particles:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), 2)
        
        food.render(screen)
        snake.render(screen)
        
        # Tampilkan skor
        score_text = font_medium.render(f"Score: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if game_over:
            show_game_over(screen, last_score)
        
        pygame.display.update()
        clock.tick(snake.speed)

if __name__ == "__main__":
    import math  # Untuk efek sparkle makanan
    main()