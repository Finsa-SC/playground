from time import sleep
import random

try:
    for _ in range(10):
        num = random.random()
        print(num)
        if 0.1 >= num:
            raise ValueError("This number is cursed")
        sleep(0.5)
except Exception as e:
    print(f"This is from exception: {e}")
else:
    print("This is from else")
finally:
    print("Program finished")
