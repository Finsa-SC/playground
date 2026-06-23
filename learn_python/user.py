from enum import Enum, auto
import random

class Difficulty(Enum):
  Easy = auto()
  Normal = auto()
  Hard = auto()

class Operator:
  def __init__(self):
    self.operator_list = ["+", "-", "/", "*"]
  
  def get_random_operator(self) -> str:
    return random.choices(self.operator_list)

  def operator(self, x, y) -> int:
    op = self.get_random_operator()
    match op:
      case '+':
        return x + y
      case '-':
        return x - y
      case '*':
        return x * y
      case '/':
        return x // y
      case _:
        return 0
        
class MathGame:
  def __init__(self):
    self.score = 0
    self.correct = 0
    self.wrong = 0

  # Get random question by difficulty
  def get_question(self, difficulty: Difficulty) -> tuple(str, int): #str for question, int for answer
    first_number: int = 0
    second_number: int = 0
    
    match difficulty:
      case Difficulty.Easy:
      
      
