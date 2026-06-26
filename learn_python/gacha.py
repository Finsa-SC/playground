import random
from time import sleep

item = ["sword", "catalyst", "shield", "polearn", "hammer", "claymore", "bow"]

selected_item = random.choices(item, k=3)

for i in range(60):
    print("\033[H\033[J", end="")

    if i <= 20:
        item1 = random.choice(item)
    if i <= 40:
        item2 = random.choice(item)
    if i <= 60:
        item3 = random.choice(item)

    i += 1
    print(f"{'':<4}{item1:<30}{item2:<30}{item3:<30}\nPull: {i}")
    sleep(0.1)
