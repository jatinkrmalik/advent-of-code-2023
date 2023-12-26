# Day 17: Clumsy Crucible

import sys
from enum import Enum
from queue import PriorityQueue
from collections import defaultdict


# Define the Direction Enum for clarity and ease of use
class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


# Define allowed turns for the crucible from each direction
ALLOWED_CRUCIBLE_TURNS = {
    Direction.RIGHT: [Direction.UP, Direction.DOWN],
    Direction.LEFT: [Direction.UP, Direction.DOWN],
    Direction.UP: [Direction.LEFT, Direction.RIGHT],
    Direction.DOWN: [Direction.LEFT, Direction.RIGHT],
}


# Function to find the minimum heat loss for moving the crucible
def find_min_heat_loss(grid, blocks_before_turn, max_in_direction):
    # Initialize distance dictionary with max values for each direction
    memo = defaultdict(lambda: defaultdict(lambda: sys.maxsize))

    for direction in Direction:
        memo[(0, 0)][direction] = 0

    # Initialize the priority queue for Dijkstra's algorithm
    pq = PriorityQueue()

    # seed pq with all possible directions from the starting position
    pq.put((0, (0, 0), Direction.RIGHT.name))
    pq.put((0, (0, 0), Direction.DOWN.name))

    while not pq.empty():
        heat_loss, position, dir_name = pq.get()
        direction = Direction[dir_name]  # Convert back to Direction enum

        # Skip if the current path's heat loss is not better than already known
        if heat_loss > memo[position][direction]:
            continue

        x, y = position
        for block in range(max_in_direction):
            # Move in the current direction
            dx, dy = direction.value
            x, y = x + dx, y + dy

            # Check if the new position is out of bounds
            if x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid):
                break

            # Accumulate heat loss
            heat_loss += grid[y][x]

            # Check if the crucible has moved the required blocks before turning
            if block < blocks_before_turn:
                continue

            # Explore new directions from the current position
            for new_dir in ALLOWED_CRUCIBLE_TURNS[direction]:
                if heat_loss < memo[(x, y)][new_dir]:
                    memo[(x, y)][new_dir] = heat_loss
                    pq.put((heat_loss, (x, y), new_dir.name))

    # Return the minimum heat loss to reach the bottom-right corner
    return min(memo[(len(grid[0]) - 1, len(grid) - 1)].values())


def parse_grid(input_str):
    return [[int(x) for x in line] for line in input_str.split("\n")]


def part_one():
    with open("day_17/input.txt", "r") as f:
        grid = parse_grid(f.read())
    min_heat_loss = find_min_heat_loss(grid, 0, 3)
    print(f"❗️ Minimum heat loss for Normal Crucible: {min_heat_loss}")


def part_two():
    with open("day_17/input.txt", "r") as f:
        grid = parse_grid(f.read())
    min_heat_loss = find_min_heat_loss(grid, 3, 10)
    print(f"❗️❗️ Minimum heat loss for Ultra Crucible: {min_heat_loss}")


def test_get_min_heat_loss_path_normal_crucible():
    input_str = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
    grid = parse_grid(input_str)
    min_heat_loss = find_min_heat_loss(grid, 0, 3)
    assert min_heat_loss == 102, f"Expected 102, got {min_heat_loss}"
    print("✅ get_min_heat_loss_path() tests passed for Crucible!")

def test_get_min_heat_loss_path_ultra_crucible():
    input_str = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
    grid = parse_grid(input_str)
    min_heat_loss = find_min_heat_loss(grid, 3, 10)
    assert min_heat_loss == 94, f"Expected 94, got {min_heat_loss}"
    print("✅ get_min_heat_loss_path() tests passed for Ultra Crucible!")


if __name__ == "__main__":
    test_get_min_heat_loss_path_normal_crucible()
    part_one()

    test_get_min_heat_loss_path_ultra_crucible()
    part_two()
