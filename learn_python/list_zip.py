#!/usr/bin/uv

orang_indo    = ['agus', 'ahmadi', 'ridwan', 'joko']
orang_eng = ['stephen', 'michael', 'jordi']

orang_orang = orang_eng + orang_indo
orang_indo_eng = list(zip(orang_indo, orang_eng))

print(orang_indo_eng)
print(orang_orang)
