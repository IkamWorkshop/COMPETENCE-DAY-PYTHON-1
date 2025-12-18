import turtle
import random

def draw_spiral():
    # Setup layar
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Spiral Warna-warni")

    # Setup turtle
    t = turtle.Turtle()
    t.speed(0)  # Kecepatan maksimal
    t.width(2)

    # Daftar warna
    colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]

    # Fungsi untuk menggambar spiral
    def draw_spiral_shape(steps, angle, step_size):
        for i in range(steps):
            t.color(colors[i % len(colors)])
            t.forward(i * step_size)
            t.right(angle)

    # Menggambar spiral pertama
    draw_spiral_shape(100, 91, 2)  # Menggunakan sudut 91 derajat untuk pola yang menarik

    # Fungsi untuk mengubah warna secara acak
    def change_colors():
        t.color(random.choice(colors))
        screen.ontimer(change_colors, 100)  # Setiap 100 ms

    # Fungsi untuk mengubah kecepatan
    def change_speed():
        t.speed(random.randint(1, 10))
        screen.ontimer(change_speed, 1000)

    # Mulai perubahan warna dan kecepatan
    change_colors()
    change_speed()

    # Interaksi: tekan spasi untuk mengubah arah
    def change_direction():
        t.right(90)  # Belok 90 derajat

    screen.onkey(change_direction, "space")
    screen.listen()

    # Klik untuk menambahkan lingkaran
    def add_circle(x, y):
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.color(random.choice(colors))
        t.circle(random.randint(10, 50))

    screen.onclick(add_circle)

    turtle.done()

if __name__ == "__main__":
    draw_spiral()