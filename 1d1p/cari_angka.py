import random

class GuestNumber:
  def __init__(self):
    self.answer = {}
    self.user_guest = []
    self.total_guest = 0
    
  def get_random(self):
    guestion = ["A", "B", "C", "D"]
    for i in range(4):
      self.answer[i] = random.choice(guestion)

  def match_guestion(self, seq) -> int:
    if self.answer[seq] == self.user_guest[seq]:
      return 1
    else:
      return 0

  def guest_number(self):
    guestion = input("Guestion: ")
    self.user_guest = []
    self.user_guest = [i for i in guestion]

    correct = 0
    for i in range(4):
      correct += self.match_guestion(i)

    self.total_guest += 1
    if correct == 4:
      print(f"Guested in {self.total_guest}")
      exit(0)
    print(f"{correct} correct")
        
if __name__ == "__main__":
  play = GuestNumber()
  play.get_random()

  for _ in range(10):
    play.guest_number()
  print(play.answer)
