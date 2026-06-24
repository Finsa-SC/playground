import random
from enum import Enum, auto

class StatusHero(Enum):
    Idle = auto()
    Defend = auto()
    Critical = auto()

class TurnBaseMechanic:
    def attack(self, hero1, hero2):
        damage = hero1.damage

        if self.critical_hit(hero1.critical_rate):
            damage *= 2
            hero1.critical_rate = 1.0
        else:
            hero1.critical_rate += random.randint(1, 10)

        if hero1.status == StatusHero.Defend:
            self.defend(hero1, hero2, damage)
        else:
            hero2.health -= damage

    @staticmethod
    def critical_hit(critical_rate: float) -> bool:
        if critical_rate >= random.randint(0, 100):
            return True
        return False

    @staticmethod
    def defend(hero1, hero2, damage):
        rng = random.randint(1, 100)
        if rng <= 30:
            hero2.health -= damage
        elif rng <= 90:
            hero2.health -= damage / hero1.defend
        else:
            hero1.health -= damage

    @staticmethod
    def set_status(hero, status: StatusHero):
        match status:
            case StatusHero.Idle:
                hero.status = StatusHero.Idle
            case StatusHero.Defend:
                hero.status = StatusHero.Defend
            case StatusHero.Critical:
                hero.status = StatusHero.Critical