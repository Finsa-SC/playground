import random
from enum import Enum, auto

class Vision(Enum):
    Pyro = auto()
    Cryo = auto()
    Geo = auto()
    Hydro = auto()
    Dendro = auto()
    Electro = auto()

rateup_character = {
    "Albedo": {
        "rarity": "★★★★★",
        "vision": Vision.Geo,
    },
}

legendary_character = {
    "Diluc": {
        "rarity": "★★★★★",
        "vision": Vision.Pyro,
    },
    "Mona": {
        "rarity": "★★★★★",
        "vision": Vision.Hydro,
    },
    "Keqing": {
        "rarity": "★★★★★",
        "vision": Vision.Electro,
    },
    "Tignari": {
        "rarity": "★★★★★",
        "vision": Vision.Dendro,
    },
    "Qiqi": {
        "rarity": "★★★★★",
        "vision": Vision.Cryo,
    },
}

basic_character = {
    "Bennet": {
        "rarity": "★★★★",
        "vision": Vision.Pyro,
    },
    "Amber": {
        "rarity": "★★★★",
        "vision": Vision.Pyro,
    },
    "Gaming": {
        "rarity": "★★★★",
        "vision": Vision.Pyro,
    },
    "Barbara": {
        "rarity": "★★★★",
        "vision": Vision.Hydro,
    },
    "Charlotte": {
        "rarity": "★★★★",
        "vision": Vision.Cryo,
    },
    "Xingqiu": {
        "rarity": "★★★★",
        "vision": Vision.Hydro,
    },
    "Kuki Shinobu": {
        "rarity": "★★★★",
        "vision": Vision.Electro,
    },
}

medium_weapon = {
    "Excalibur Sword": {
        "rarity": "★★",
    },
    "Black Sword": {
        "rarity": "★★",
    },
    "Milk Claymore": {
        "rarity": "★★",
    },
    "Wild of Catalyst": {
        "rarity": "★★",
    },
    "Cup of Catalyst": {
        "rarity": "★★",
    },
    "Greater Catalyst": {
        "rarity": "★★",
    },
    "Frozen Polearn": {
        "rarity": "★★",
    },
    "Spoon of Polearn": {
        "rarity": "★★",
    },
    "Gigaban Sword": {
        "rarity": "★★",
    },
}

basic_weapon = {
    "Ambatukan Sword": {
        "rarity": "★",
    },
    "Artur Sword": {
        "rarity": "★",
    },
    "Grow Bow": {
        "rarity": "★",
    },
    "Note Catalyst": {
        "rarity": "★",
    },
    "Fahfah Sword": {
        "rarity": "★",
    },
    "Speaker Claymore": {
        "rarity": "★",
    },
    "It's Sword": {
        "rarity": "★",
    },
    "Is it Polearn": {
        "rarity": "★",
    },
}


def get_item(rarity: str) -> dict[str, dict]:
    if rarity == "low":
        return random.choice([basic_weapon.items(), medium_weapon.items()])
    elif rarity == "medium":
        return random.choice([basic_character])
    elif rarity == "high":
        if random.random() <= 0.5:
            return random.choice([rateup_character])
        else:
            return random.choice([legendary_character])
    else:
        raise ValueError("Invalid Value for rarity")

item = [rateup_character, legendary_character, basic_character, medium_weapon, basic_weapon]

chance = ["low", "medium", "high"]
weight = [91, 8.8, 0.2]

item_rarity = []
for i in range(10):
    if i == 9: # Jaminan b4 setiap 10 pull
        item_rarity.append("medium")
        continue

    item_rarity.extend(random.choices(chance, weight))

print(legendary_character.items())

for rarity in item_rarity:
    items = get_item(rarity)
    # print(type(items))
    # print(f"{items}")
