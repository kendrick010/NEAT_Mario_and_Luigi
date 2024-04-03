from enum import Enum
from queue import PriorityQueue

class Character(Enum):
    MARIO = 1
    LUIGI = 2
    BABY_MARIO = 3
    BABY_LUIGI = 4
    EMPTY = 5

# Example usage
character_queue = PriorityQueue()
# character_queue.push(item=Character.EMPTY, priority=2)
# character_queue.push(item=Character.EMPTY, priority=2)
# character_queue.push(item=Character.EMPTY, priority=2)
# character_queue.push(item=Character.EMPTY, priority=2)
# character_queue.push(item=Character.MARIO, priority=1)

character_queue.put((1, Character.EMPTY))
character_queue.put((1, Character.EMPTY))
print(list(character_queue.get()))
