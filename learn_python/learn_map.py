#!/usr/bin/uv

# Map with lambda ============================================
angka = [1, 2, 3, 4, 5]

kali = list(map(lambda a: a * 2, angka))

#print(kali)


# Map with function =========================================
def modulus(x):
  return x % 2 != 0

ganjil = list(map(modulus, angka))
print(ganjil)


# Map converter ==============================================
nama = ["agus", "rahmat", "joko"]
kapital = list(map(str.title, nama))
print(kapital)
