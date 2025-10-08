import random
from collections import deque
from snake.logic import GameState, Turn, Snake, Direction

"""
Your mission, should you choose to accept it, is to write the most cracked snake AI possible.

All the info you'll need to do this is in the GameState and Snake classes in snake/logic.py

Below is all of the data you'll need, and some small examples that you can uncomment and use if you want :)

"""


def myAI(state: GameState) -> Turn:

    grid_width: int = state.width
    grid_height: int = state.height
    food: set = state.food
    walls: set = state.walls
    my_snake: Snake = state.snake
    my_snake_direction: Direction = Direction(state.snake.direction)
    my_snake_body: list = list(state.snake.body)
    enemy_snakes = state.enemies

    # All occupied cells
    occupied = set(walls)
    for s in [my_snake] + enemy_snakes:
        if s.isAlive:
            occupied |= set(s.body)

    # Helper to check if a cell is safe
    def is_safe(cell):
        x, y = cell
        return 0 <= x < grid_width and 0 <= y < grid_height and cell not in occupied

    # BFS to find shortest path to any food
    from collections import deque
    def bfs(start, targets):
        queue = deque()
        queue.append((start, []))
        visited = set()
        visited.add(start)
        while queue:
            pos, path = queue.popleft()
            if pos in targets:
                return path
            for turn in [Turn.LEFT, Turn.STRAIGHT, Turn.RIGHT]:
                # Simulate move
                dir_idx = (my_snake.direction + turn.value) % 4 if not path else (my_snake.direction + sum([t.value for t in path + [turn]])) % 4
                dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][dir_idx]
                next_pos = (pos[0] + dx, pos[1] + dy)
                if next_pos not in visited and is_safe(next_pos):
                    queue.append((next_pos, path + [turn]))
                    visited.add(next_pos)
        return None

    # Try to find path to food
    path = bfs(my_snake.head, food)
    if path:
        return path[0]

    # If no path to food, pick any safe move
    for turn in [Turn.LEFT, Turn.STRAIGHT, Turn.RIGHT]:
        next_head = my_snake.get_next_head(turn)
        if is_safe(next_head):
            return turn

    #saved
    # No safe moves, just go straight
    return Turn.STRAIGHT
    
    return random.choice(list(Turn))

    # ======================================
    # =       Try out some examples!       =
    # ======================================

    # from examples.dumbAI import dumbAI
    # return dumbAI(state)

    #from examples.smartAI import smartAI
    #return smartAI(state)
