from collections import deque
from enum import Enum


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)


REVERSE_DIRECTION_MAP = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}


PIPE_MOVEMENT_OPTIONS = {
    "|": [Direction.NORTH, Direction.SOUTH],
    "-": [Direction.EAST, Direction.WEST],
    "L": [Direction.NORTH, Direction.EAST],
    "J": [Direction.NORTH, Direction.WEST],
    "7": [Direction.SOUTH, Direction.WEST],
    "F": [Direction.SOUTH, Direction.EAST],
    "S": [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST],
}


def parse_maze(input_string):
    return [list(line) for line in input_string.splitlines()]


def find_animal_start(maze):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == "S":
                return (i, j)


def find_cycle(start, maze):
    stack = [start]
    visited = {start}
    path_tracker = {start: None}

    while stack:
        (x, y) = stack.pop()

        for direction in PIPE_MOVEMENT_OPTIONS[maze[x][y]]:
            nx, ny = x + direction.value[0], y + direction.value[1]
            if (
                (0 <= nx < len(maze))
                and (0 <= ny < len(maze[0]))
                and (maze[nx][ny] in PIPE_MOVEMENT_OPTIONS)
                and (REVERSE_DIRECTION_MAP[direction] in PIPE_MOVEMENT_OPTIONS[maze[nx][ny]])
            ):
                if (nx, ny) not in visited:
                    stack.append((nx, ny))
                    visited.add((nx, ny))
                    path_tracker[(nx, ny)] = (x, y)
                    break

                elif path_tracker[(x, y)] != (nx, ny):
                    cycle = [(nx, ny)]  # We've found a cycle
                    while (x, y) != (nx, ny):
                        cycle.append((x, y))
                        x, y = path_tracker[(x, y)]
                    return cycle

    # Raise error in case no cycle is found
    raise ValueError("No cycle found")


def get_steps_to_the_farthest_point(cycle):
    return len(cycle) // 2



def part_one():
    with open("day_10/input.txt") as f:
        maze = parse_maze(f.read())
    start = find_animal_start(maze)
    cycle = find_cycle(start, maze)
    farthest_point = get_steps_to_the_farthest_point(cycle)
    print(f"Steps to the farthest point: {farthest_point}")


def test_simple_maze():
    maze = """.....
.S-7.
.|.|.
.L-J.
....."""
    maze = [row for row in maze.splitlines()]
    start = find_animal_start(maze)
    cycle = find_cycle(start, maze)
    print(f"Cycle: {cycle}")
    farthest_point = get_steps_to_the_farthest_point(cycle)
    assert farthest_point == 4, f"Expected 4, got {farthest_point}"
    print("✅ Simple maze test passed")


def test_complex_maze():
    maze = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
    maze = parse_maze(maze)
    start = find_animal_start(maze)
    cycle = find_cycle(start, maze)
    print(f"Cycle: {cycle}")
    farthest_point = get_steps_to_the_farthest_point(cycle)
    assert farthest_point == 4, f"Expected 4, got {farthest_point}"
    print("✅ Complex maze test passed")

def test_more_complex_maze():
    maze = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
    maze = parse_maze(maze)
    start = find_animal_start(maze)
    cycle = find_cycle(start, maze)
    print(f"Cycle: {cycle}")
    farthest_point = get_steps_to_the_farthest_point(cycle)
    assert farthest_point == 8, f"Expected 8, got {farthest_point}"
    print("✅ More complex maze test passed")

def test_most_complex_maze():
    maze = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
    maze = parse_maze(maze)
    start = find_animal_start(maze)
    cycle = find_cycle(start, maze)
    print(f"Cycle: {cycle}")
    farthest_point = get_steps_to_the_farthest_point(cycle)
    assert farthest_point == 8, f"Expected 8, got {farthest_point}"
    print("✅ Most complex maze test passed")


if __name__ == "__main__":
    test_simple_maze()
    test_complex_maze()
    test_more_complex_maze()
    test_most_complex_maze()

    part_one()
