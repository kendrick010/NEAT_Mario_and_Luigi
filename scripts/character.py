from enum import Enum

class Character(Enum):
    MARIO = 1
    LUIGI = 2
    BABY_MARIO = 3
    BABY_LUIGI = 4
    EMPTY = 5

    def __lt__(self, other):
        if self == Character.EMPTY or other == Character.EMPTY:
            return False
        
        return True