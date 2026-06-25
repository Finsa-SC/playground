import random
import string
from enum import Enum
from time import sleep
from random_word import RandomWords


class Enemy(Enum):
    John = {
        "desc": "John is a villager",
        "wpm": 18,
        "accuracy": 72,
        "start_delay": (1.8, 3.2),
        "panic": 2
    }

    Marlo = {
        "desc": "Marlo is a construction worker",
        "wpm": 28,
        "accuracy": 76,
        "start_delay": (1.3, 2.4),
        "panic": 2
    }

    Juliana = {
        "desc": "Juliana is an office worker",
        "wpm": 42,
        "accuracy": 82,
        "start_delay": (1.02, 1.88),
        "panic": 2
    }

    Edward = {
        "desc": "Edward is a skilled programmer",
        "wpm": 63,
        "accuracy": 90,
        "start_delay": (0.82, 1.48),
        "panic": 2
    }

    Bastian = {
        "desc": "Bastian is a senior programmer",
        "wpm": 92,
        "accuracy": 95,
        "start_delay": (0.42, 0.88),
        "panic": 2
    }

    Finn = {
        "desc": "Finn is a legendary keyboard warrior",
        "wpm": 125,
        "accuracy": 98,
        "start_delay": (0.18, 0.8),
        "panic": 2
    }

class TypingBot:
    def __init__(self):
        self.opp_name = ""
        self.opp_wpm = 0
        self.opp_accuracy = 0
        self.opp_start_delay = (0, 0)

    def select_bot(self):
        print("Select your opponent")
        for i, j in enumerate(Enemy, start=1):
            print(f"{i}. {j.value['desc']}")
        str_opp_num = input("Input number of your opponent: ")

        if str_opp_num.isdigit():
            opp_num = int(str_opp_num)

            print(len(Enemy))
            if 1 <= opp_num <= len(Enemy):
                opponent = list(Enemy)[opp_num - 1]
                self.opp_name = opponent.name
                self.opp_wpm = opponent.value['wpm']
                self.opp_accuracy = opponent.value['accuracy']
                self.opp_start_delay = opponent.value['start_delay']
            else:
                raise IndexError("Your input is out of range")
        else:
            raise ValueError("Invalid input")

    def bot_typing(self, word: str):
        word = list(word)
        word_len = len(word)
        current_delay = 60 / (self.opp_wpm * 5)

        typed = []
        sleep(random.uniform(*self.opp_start_delay))
        for i in range(0, word_len):
            print("\033[H\033[J", end="")
            if self.accuracy():
                typed.append(word[i])
            else:
                typed.append(random.choice(string.ascii_letters))
            print("".join(typed))
            sleep(current_delay)

    def accuracy(self) -> bool:
        return self.opp_accuracy >= random.uniform(1, 100)

    def __str__(self):
        return f"Your opponent is {self.opp_name}, {self.opp_wpm} wpm with {self.opp_accuracy}% accuracy"

if __name__ == "__main__":
    typing = TypingBot()

    print("\033[H\033[J", end="")
    typing.select_bot()

    print("\033[H\033[J", end="")
    print(typing)

    rword = RandomWords().get_random_word()
    typing.bot_typing(rword)
    print("The word is: " + rword)