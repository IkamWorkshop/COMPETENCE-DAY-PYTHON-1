import pygame
import random
import sys

# inisialisasi pygame
pygame.init()

# ukuran layar
lebar = 800
tinggi = 600
layar = pygame.display.set_mode((lebar, tinggi))
pygame.display.set_caption("tangkap buah 🍎🍌💣")

# warna
warna_latar = (240, 248, 255)  # biru muda
warna_keranjang = (100, 200, 100)
warna_teks = (50, 50, 50)

# emoji untuk buah dan bom
buah_emoji = ["🍎", "🍌", "🍒", "🍇", "🍉", "🍓", "🥭"]
bom_emoji = "💣"

# font untuk emoji dan teks
font_emoji = pygame.font.SysFont("segoeuiemoji", 48)
font_teks = pygame.font.SysFont("arial", 28)

# posisi keranjang
keranjang_x = lebar // 2
keranjang_y = tinggi - 80
lebar_keranjang = 120
tinggi_keranjang = 60

# kecepatan awal
kecepatan_awal = 3

# daftar objek yang jatuh
objek_jatuh = []

# skor
skor = 0

# efek lambat setelah kena bom
efek_lambat = 0
waktu_efek = 0

# fungsi buat objek baru
def buat_objek():
    if random.random() < 0.3:  # 30% kemungkinan bom
        emoji = bom_emoji
        jenis = "bom"
    else:  # 70% kemungkinan buah
        emoji = random.choice(buah_emoji)
        jenis = "buah"
    
    x = random.randint(50, lebar - 50)
    y = -50
    kecepatan = random.uniform(kecepatan_awal, kecepatan_awal + 2)
    
    objek_jatuh.append({
        "emoji": emoji,
        "jenis": jenis,
        "x": x,
        "y": y,
        "kecepatan": kecepatan
    })

# fungsi gambar keranjang
def gambar_keranjang():
    # gambar kotak keranjang
    pygame.draw.rect(layar, warna_keranjang, 
                    (keranjang_x - lebar_keranjang//2, keranjang_y, 
                     lebar_keranjang, tinggi_keranjang), 0, 15)
    pygame.draw.rect(layar, (80, 180, 80), 
                    (keranjang_x - lebar_keranjang//2, keranjang_y, 
                     lebar_keranjang, tinggi_keranjang), 3, 15)
    
    # gambar emoji keranjang
    teks_keranjang = font_emoji.render("🧺", True, warna_teks)
    layar.blit(teks_keranjang, (keranjang_x - 25, keranjang_y + 5))

# fungsi gambar efek lambat
def gambar_efek_lambat():
    if efek_lambat > 0:
        # buat semi transparan
        s = pygame.Surface((lebar, tinggi), pygame.SRCALPHA)
        s.fill((255, 100, 100, 50))  # merah transparan
        layar.blit(s, (0, 0))
        
        # teks peringatan
        teks = font_teks.render("hati-hati! kecepatan lambat", True, (200, 50, 50))
        layar.blit(teks, (lebar//2 - 150, 20))

# fungsi tampilkan skor
def tampilkan_skor():
    # panel skor
    pygame.draw.rect(layar, (255, 255, 200), (10, 10, 200, 80), 0, 10)
    pygame.draw.rect(layar, (200, 200, 150), (10, 10, 200, 80), 2, 10)
    
    # teks skor
    teks_skor = font_teks.render(f"skor: {skor}", True, warna_teks)
    layar.blit(teks_skor, (30, 25))
    
    # teks efek
    if efek_lambat > 0:
        teks_efek = font_teks.render(f"efek: {efek_lambat}s", True, (200, 50, 50))
        layar.blit(teks_efek, (30, 55))

# fungsi tampilkan petunjuk
def tampilkan_petunjuk():
    petunjuk = [

    ]
    
    for i, teks in enumerate(petunjuk):
        render = font_teks.render(teks, True, warna_teks)
        layar.blit(render, (lebar//2 - 200, tinggi - 120 + i*30))

# timer untuk buat objek baru
pygame.time.set_timer(pygame.USEREVENT, 800)

# clock untuk fps
clock = pygame.time.Clock()
fps = 60

# status pause
pause = False

# loop utama
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.USEREVENT and not pause:
            buat_objek()
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
            
            if event.key == pygame.K_ESCAPE:
                running = False
    
    if not pause:
        # input keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and keranjang_x > lebar_keranjang//2:
            keranjang_x -= 8
        if keys[pygame.K_RIGHT] and keranjang_x < lebar - lebar_keranjang//2:
            keranjang_x += 8
        
        # update efek lambat
        if efek_lambat > 0:
            efek_lambat -= 1/fps
            if efek_lambat < 0:
                efek_lambat = 0
        
        # update posisi objek jatuh
        for objek in objek_jatuh[:]:
            # hitung kecepatan dengan efek lambat
            kecepatan_sekarang = objek["kecepatan"]
            if efek_lambat > 0:
                kecepatan_sekarang *= 0.5  # jadi setengah kecepatan
            
            objek["y"] += kecepatan_sekarang
            
            # cek tabrakan dengan keranjang
            keranjang_rect = pygame.Rect(
                keranjang_x - lebar_keranjang//2,
                keranjang_y,
                lebar_keranjang,
                tinggi_keranjang
            )
            
            objek_rect = pygame.Rect(
                objek["x"] - 25,
                objek["y"] - 25,
                50, 50
            )
            
            if keranjang_rect.colliderect(objek_rect):
                if objek["jenis"] == "buah":
                    skor += 10
                    # efek suara positif
                    pygame.mixer.Sound.play(pygame.mixer.Sound(
                        pygame.mixer.Sound(b'')  # dummy sound
                    ))
                else:  # bom
                    skor -= 20
                    if skor < 0:
                        skor = 0
                    efek_lambat = 3  # efek lambat 3 detik
                    # efek suara negatif
                    pygame.mixer.Sound.play(pygame.mixer.Sound(
                        pygame.mixer.Sound(b'')
                    ))
                
                objek_jatuh.remove(objek)
            
            # hapus jika keluar layar
            elif objek["y"] > tinggi + 50:
                objek_jatuh.remove(objek)
    
    # gambar latar
    layar.fill(warna_latar)
    
    # gambar awan atau dekorasi
    for i in range(5):
        x = (i * 200 + pygame.time.get_ticks()//50) % (lebar + 400) - 200
        y = 100 + (i * 30) % 100
        awan = font_emoji.render("☁️", True, (200, 230, 255))
        layar.blit(awan, (x, y))
    
    # gambar semua objek jatuh
    for objek in objek_jatuh:
        teks_emoji = font_emoji.render(objek["emoji"], True, warna_teks)
        layar.blit(teks_emoji, (objek["x"] - 25, objek["y"] - 25))
        

    
    # gambar keranjang
    gambar_keranjang()
    
    # gambar efek lambat jika ada
    gambar_efek_lambat()
    
    # tampilkan skor
    tampilkan_skor()
    
    # tampilkan petunjuk
    tampilkan_petunjuk()
    
    # tampilkan status pause
    if pause:
        overlay = pygame.Surface((lebar, tinggi), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        layar.blit(overlay, (0, 0))
        
        teks_pause = font_teks.render("game paused", 
                                     True, (255, 255, 255))
        layar.blit(teks_pause, (lebar//2 - 200, tinggi//2 - 20))
    
    # update layar
    pygame.display.flip()
    
    # kontrol fps
    clock.tick(fps)

# keluar dari game
pygame.quit()
sys.exit()