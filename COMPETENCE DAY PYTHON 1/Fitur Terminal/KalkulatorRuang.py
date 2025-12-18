#sentra
print("MENGHITUNG BANGUN RUANG")
print("PILIHLAH BANGUN RUANG YANG TERSEDIA  \nbalok    kubus    tabung    \nkerucut    bola    prisma")
ingin = input("ingin menghitung apa? ", )#balok, kubus, tabung, kerucut, bola , prisma
if ingin == "balok":
    p = float(input("masukkan panjang balok: "))
    l = float(input("masukkan lebar balok: "))
    t = float(input("masukkan tinggi balok: "))
    v = p * l * t
    print("volume balok adalah: ", v)
    lp = 2 * (p * l + p * t + l * t)
    print("luas permukaan balok adalah: ", lp)
elif ingin == "kubus":
    s = float(input("masukkan sisi kubus: "))
    v = s * s * s
    print("volume kubus adalah: ", v)
    lp = 6 * (s * s)
    print("luas permukaan kubus adalah: ", lp)
elif ingin == "tabung":
    r = float(input("masukkan jari-jari tabung: "))
    t = float(input("masukkan tinggi tabung: "))
    v = 3.14 * r * r * t
    print("volume tabung adalah: ", v)
    lp = 2 * 3.14 * r * (r + t)
    print("luas permukaan tabung adalah: ", lp)
elif ingin == "kerucut":
    r = float(input("masukkan jari-jari kerucut: "))
    t = float(input("masukkan tinggi kerucut: "))
    s = float(input("masukkan sisi kerucut: "))
    v = 1 / 3 * 3.14 * r * r * t
    print("volume kerucut adalah: ", v)
    lp = 3.14 * r * (r + s)
    print("luas permukaan kerucut adalah: ", lp)
elif ingin == "bola":
    r = float(input("masukkan jari-jari bola: "))
    v = 4 / 3 * 3.14 * r * r * r
    print("volume bola adalah: ", v)
    lp = 4 * 3.14 * r * r
    print("luas permukaan bola adalah: ", lp)
elif ingin == "prisma":
    a = float(input("masukkan luas alas prisma: "))
    t = float(input("masukkan tinggi prisma: "))
    lp_alas = float(input("masukkan luas permukaan alas prisma: "))
    lp_sisi = float(input("masukkan luas permukaan sisi prisma: "))
    v = a * t
    print("volume prisma adalah: ", v)
    lp = 2 * lp_alas + lp_sisi
    print("luas permukaan prisma adalah: ", lp)
else:
    print("maaf bangun ruang yang anda masukkan tidak tersedia")    