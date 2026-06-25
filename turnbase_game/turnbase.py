import random

from attributes import Attribute
from mechanic import TurnBaseMechanic, StatusHero

class TurnBaseGames:
  def __init__(self):
    self.match = TurnBaseMechanic()
    self.my_hero = Attribute()
    self.opponent = Attribute()

  def play(self):
    self.match.attack(self.my_hero, self.opponent)
    self.match.attack(self.opponent, self.my_hero)

    self.match.set_status(self.my_hero, status=StatusHero.Defend)
    self.match.attack(self.opponent, self.my_hero)
  def __str__(self):
    return f"""Your Hero has {self.my_hero.health} health, {self.my_hero.damage} damage and {self.my_hero.critical_rate} critical chance\nYour opponent has {self.opponent.health} health, {self.opponent.damage} damage and {self.opponent.critical_rate} critical chance"""

    
if __name__ == "__main__":
  play = TurnBaseGames()

  play.play()
  print(play.__str__())

  print("\n=============Match 2=================")
  play.play()
  print(play.__str__())
  print(play.my_hero.status)
