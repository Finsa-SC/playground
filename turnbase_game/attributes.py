from mechanic import StatusHero

class Attribute:
  def __init__(self):
    self.health = 100.0
    self.damage = 1.0
    self.critical_rate = 1.0
    self.defend = 1.0
    self.status = StatusHero.Idle