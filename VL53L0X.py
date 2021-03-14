from enum import Enum

"""
PC VL53L0X Stub (DO NOT USE)
"""

class Vl53l0xAccuracyMode(Enum):
    GOOD = 0        # 33 ms timing budget 1.2m range
    BETTER = 1      # 66 ms timing budget 1.2m range
    BEST = 2        # 200 ms 1.2m range
    LONG_RANGE = 3  # 33 ms timing budget 2m range
    HIGH_SPEED = 4  # 20 ms timing budget 1.2m range

class VL53L0X:
    def __init__(self, **kwarg):
        pass
    def open(self):
        pass
    def start_ranging(self, mode: Vl53l0xAccuracyMode):
        pass
    def get_timing(self):
        return 0
    def get_distance(self):
        return 0
    def stop_ranging(self):
        pass
    def close(self):
        pass