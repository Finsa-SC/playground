from enum import Enum

class Ligth(Enum):
    Green = "MOVE"
    Yellow = "PREPARE"
    Red = "STOP"

class LightSystem:
    def change_light(self, direction):
        direction

class TrafficLight:
    def __init__(self):
        self.north = {
            "vehicle": 0,
            "skip": 0,
            "light": Ligth.Red,
        }
        self.east = {
            "vehicle": 0,
            "skip": 0,
            "light": Ligth.Red,
        }
        self.south = {
            "vehicle": 0,
            "skip": 0,
            "light": Ligth.Red,
        }
        self.west = {
            "vehicle": 0,
            "skip": 0,
            "light": Ligth.Red,
        }