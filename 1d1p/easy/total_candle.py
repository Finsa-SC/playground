candles = [1, 2, 3, 5, 5, 2, 1]

count = 0
highest = 0
for candle in candles:
  if candle > highest:
    highest = candle
    count = 1
  elif candle == highest:
    count += 1

print(count)
