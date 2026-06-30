# Nama Project

## Problem
Smart traffic light, tidak menggunakan input karena otomatis, dan outputnya cukup terminal dengan art traffic

## Features
- 🔴 Detect vehicle count
- 🔴 increase priority for busy traffic
- 🟡 add priority every traffic has skip
- 🟢 terminal design

## Struktur
- main.py

## Alur
- terdapat 4 direction (timur, selatan, utara, barat)
- lampu tidak menyala berurutan, tapi mencari traffic paling padat
- jika ada traffic yang padat, prioritas green light akan diberikan ke busy traffic
- setiap traffic yang tidak menapat hijau akan menambah poin skip yang akan meningkatkan priority
- ada time sleep setiap 5sec yang akan mengecek traffic, jika masih busy, maka akan tambah 5sec lagi
- min hijau=5sec, max hijau=30sec,

## Pseudocode
class TrafficLight(enum): 
    untuk traffic light (hijau, kuning, merah)

class TrafficSystem:
    untuk mengatur sistem, logika dan perubahan traffic light

class
    untuk executor dan looping traffic light

## Catatan / Ideas
not yet