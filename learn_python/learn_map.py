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

def checking(ip: str, status: str):
  print(f"{ip} -> {status}")

device = [("192.168.1.1", "200"), ("192.168.1.2", "500")]
greetings = list(map(checking, *device))

greetings = list(map(lambda x: checking(*x), device))

# Map converter ==============================================
nama = ["agus", "rahmat", "joko"]
kapital = list(map(str.title, nama))
print(kapital)
