import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta
WINDOW_SIZE = 600
GRID_SIZE = 3
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
LINE_WIDTH = 10
SYMBOL_WIDTH = 15
FONT_SIZE = 40
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)

class TicTacToe:
    def __init__(self):
        """Inisialisasi game TicTacToe"""
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
        pygame.display.set_caption("Tic Tac Toe")
        
        # Font
        self.font = pygame.font.SysFont('arial', FONT_SIZE)
        self.small_font = pygame.font.SysFont('arial', FONT_SIZE - 10)
        
        # Inisialisasi papan
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        # Pemain saat ini (X mulai duluan)
        self.current_player = 'X'
        
        # Status game
        self.game_over = False
        self.winner = None
        self.draw = False
        
        # Tombol play again
        self.button_rect = pygame.Rect(
            WINDOW_SIZE // 2 - BUTTON_WIDTH // 2,
            WINDOW_SIZE + 20,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
    
    def draw_grid(self):
        """Menggambar grid papan permainan"""
        # Garis vertikal
        for i in range(1, GRID_SIZE):
            pygame.draw.line(
                self.screen, BLACK,
                (i * CELL_SIZE, 0),
                (i * CELL_SIZE, WINDOW_SIZE),
                LINE_WIDTH
            )
        
        # Garis horizontal
        for i in range(1, GRID_SIZE):
            pygame.draw.line(
                self.screen, BLACK,
                (0, i * CELL_SIZE),
                (WINDOW_SIZE, i * CELL_SIZE),
                LINE_WIDTH
            )
    
    def draw_symbols(self):
        """Menggambar simbol X dan O pada papan"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 'X':
                    # Gambar X
                    start_x = col * CELL_SIZE + CELL_SIZE // 4
                    start_y = row * CELL_SIZE + CELL_SIZE // 4
                    end_x = (col + 1) * CELL_SIZE - CELL_SIZE // 4
                    end_y = (row + 1) * CELL_SIZE - CELL_SIZE // 4
                    
                    pygame.draw.line(
                        self.screen, RED,
                        (start_x, start_y), (end_x, end_y),
                        SYMBOL_WIDTH
                    )
                    pygame.draw.line(
                        self.screen, RED,
                        (end_x, start_y), (start_x, end_y),
                        SYMBOL_WIDTH
                    )
                
                elif self.board[row][col] == 'O':
                    # Gambar O
                    center_x = col * CELL_SIZE + CELL_SIZE // 2
                    center_y = row * CELL_SIZE + CELL_SIZE // 2
                    radius = CELL_SIZE // 3
                    
                    pygame.draw.circle(
                        self.screen, BLUE,
                        (center_x, center_y), radius,
                        SYMBOL_WIDTH
                    )
    
    def draw_status(self):
        """Menampilkan status game dan informasi pemain"""
        status_area = pygame.Rect(0, WINDOW_SIZE, WINDOW_SIZE, 100)
        pygame.draw.rect(self.screen, LIGHT_BLUE, status_area)
        
        if self.game_over:
            if self.winner:
                message = f"!"
                color = GREEN
            else:
                message = ""
                color = BLACK
        else:
            message = f"Giliran Pemain: {self.current_player}"
            color = BLACK
        
        # Render teks status
        text = self.font.render(message, True, color)
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE + 40))
        self.screen.blit(text, text_rect)
        
        # Gambar tombol play again jika game selesai
        if self.game_over:
            pygame.draw.rect(self.screen, GRAY, self.button_rect, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, self.button_rect, 2, border_radius=10)
            
            button_text = self.small_font.render("Main Lagi", True, BLACK)
            button_text_rect = button_text.get_rect(center=self.button_rect.center)
            self.screen.blit(button_text, button_text_rect)
    
    def handle_click(self, pos):
        """Menangani klik mouse"""
        x, y = pos
        
        # Jika game sudah selesai, cek apakah tombol play again diklik
        if self.game_over:
            if self.button_rect.collidepoint(x, y):
                self.reset_game()
            return
        
        # Cek jika klik di area papan
        if y < WINDOW_SIZE:
            row = y // CELL_SIZE
            col = x // CELL_SIZE
            
            # Validasi: hanya tempati jika kotak kosong
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                if self.board[row][col] == '':
                    self.board[row][col] = self.current_player
                    
                    # Cek kemenangan atau seri
                    if self.check_win(row, col):
                        self.game_over = True
                        self.winner = self.current_player
                    elif self.check_draw():
                        self.game_over = True
                        self.draw = True
                    else:
                        # Ganti giliran pemain
                        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def check_win(self, row, col):
        """Memeriksa apakah ada pemain yang menang"""
        symbol = self.board[row][col]
        
        # Cek baris
        if all(self.board[row][c] == symbol for c in range(GRID_SIZE)):
            return True
        
        # Cek kolom
        if all(self.board[r][col] == symbol for r in range(GRID_SIZE)):
            return True
        
        # Cek diagonal utama (jika posisi berada di diagonal)
        if row == col:
            if all(self.board[i][i] == symbol for i in range(GRID_SIZE)):
                return True
        
        # Cek diagonal sekunder
        if row + col == GRID_SIZE - 1:
            if all(self.board[i][GRID_SIZE - 1 - i] == symbol for i in range(GRID_SIZE)):
                return True
        
        return False
    
    def check_draw(self):
        """Memeriksa apakah game seri"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == '':
                    return False
        return True
    
    def reset_game(self):
        """Mengatur ulang game ke kondisi awal"""
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.draw = False
    
    def run(self):
        """Loop utama game"""
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Klik kiri mouse
                        self.handle_click(event.pos)
            
            # Render
            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_symbols()
            self.draw_status()
            
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    game = TicTacToe()
    game.run()