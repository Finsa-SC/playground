import random
import string
from enum import Enum
from time import sleep
from random_word import RandomWords


class Enemy(Enum):
    John = {
        "desc": "John is a villager",
        "wpm": 18,
        "accuracy": 91,
        "start_delay": (1.8, 3.2),
        "panic_multiplier": 0.35,
    }

    Marlo = {
        "desc": "Marlo is a construction worker",
        "wpm": 28,
        "accuracy": 76,
        "start_delay": (1.3, 2.4),
        "panic_multiplier": 0.29,
    }

    Juliana = {
        "desc": "Juliana is an office worker",
        "wpm": 42,
        "accuracy": 82,
        "start_delay": (1.02, 1.88),
        "panic_multiplier": 0.24,
    }

    Edward = {
        "desc": "Edward is a skilled programmer",
        "wpm": 63,
        "accuracy": 90,
        "start_delay": (0.82, 1.48),
        "panic_multiplier": 0.18,
    }

    Bastian = {
        "desc": "Bastian is a senior programmer",
        "wpm": 92,
        "accuracy": 95,
        "start_delay": (0.42, 0.88),
        "panic_multiplier": 0.12,
    }

    Finn = {
        "desc": "Finn is a legendary keyboard warrior",
        "wpm": 125,
        "accuracy": 98,
        "start_delay": (0.18, 0.8),
        "panic_multiplier": 0.05,
    }

class TypingBot:
    def __init__(self):
        self.opp_name = ""
        self.opp_wpm = 0.0
        self.opp_accuracy = 0.0
        self.opp_start_delay = (0, 0)
        self.opp_panic_multiplier = 0.0

    def select_bot(self):
        print("Select your opponent")
        for i, j in enumerate(Enemy, start=1):
            print(f"{i}. {j.value['desc']}")
        str_opp_num = input("Input number of your opponent: ")

        if str_opp_num.isdigit():
            opp_num = int(str_opp_num)

            ## Set opponent attribute
            if 1 <= opp_num <= len(Enemy):
                opponent = list(Enemy)[opp_num - 1]
                self.opp_name = opponent.name
                self.opp_wpm = opponent.value['wpm']
                self.opp_accuracy = opponent.value['accuracy']
                self.opp_start_delay = opponent.value['start_delay']
                self.opp_panic_multiplier = opponent.value['panic_multiplier']
            else:
                raise IndexError("Your input is out of range")
        else:
            raise ValueError("Invalid input")

    def bot_typing(self, word: str):
        word = list(word)
        word_len = len(word)
        base_delay = 60 / (self.opp_wpm * 5)

        typed = []
        sleep(random.uniform(*self.opp_start_delay))
        for i in range(0, word_len):
            print("\033[H\033[J", end="")
            print(self.__str__())
            current_delay = base_delay

            # Rng for panic
            if self.getting_panic(word):
                current_delay *= (1 + self.opp_panic_multiplier)

            # rng for accuracy
            if self.accuracy():
                typed.append(word[i])
            else:
                typed.append(random.choice(string.ascii_letters))

            print("".join(typed))
            sleep(current_delay)

    def accuracy(self) -> bool:
        return self.opp_accuracy >= random.uniform(1, 100)

    def getting_panic(self, word):
        chance = min(
            self.opp_panic_multiplier * (len(word) / 10),
            0.95
        )
        panic = chance > random.random()
        if panic:
            self.opp_panic_multiplier = min(
                self.opp_panic_multiplier + 0.03,
                0.95
            )

            if random.random() >= 0.5:
                penalty = random.uniform(1, 3)
            else:
                penalty = random.uniform(1, 6)
            self.opp_accuracy = max(
                self.opp_accuracy - penalty,
                0
            )

        return panic

    def __str__(self):
        return f"Your opponent is {self.opp_name}, \n{self.opp_wpm} wpm \nwith {self.opp_accuracy}% accuracy\n{self.opp_panic_multiplier} panic"

if __name__ == "__main__":
    typing = TypingBot()

    print("\033[H\033[J", end="")
    typing.select_bot()

    print("\033[H\033[J", end="")
    print(typing)

    rword = RandomWords().get_random_word()
    typing.bot_typing(rword)
    print("The word is: " + rword)