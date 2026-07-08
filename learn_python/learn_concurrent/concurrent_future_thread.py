import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep


def send_message(index: int) -> str:
    delay = random.randint(1, 10)
    sleep(delay)
    return f"Hello from server {index} with delay {delay} sec"

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(send_message, i) for i in range(10)]

    for future in as_completed(futures):
        print(future.result())