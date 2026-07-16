import random
import subprocess
from time import sleep

message = ["Hello", "My name is Finn", "Nice to meetcha", "who are you?", "I'm happy"]
title = ["System", "Browser", "PyCharm", "Discord", "Github"]
status = ["critical", "low", "normal"]

while True:
    subprocess.run(["notify-send", random.choice(title), random.choice(message), "-u", random.choice(status)])

    sleep(10)