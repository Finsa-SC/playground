angka = [1, 2, 3, 4, 5]

ganjil = filter(lambda x: x % 2 == 1, angka)

print(list(ganjil))


campuran = [1, "agus", "3", "Rahmat", "4"]
angka = list(filter(str.isdigit, map(str, campuran)))
string = list(filter(not str.isdigit, map(str, campuran)))

print(angka)
print(string)
