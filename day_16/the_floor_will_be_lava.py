# Day 16 - The Floor will be Lava

from enum import Enum
from collections import deque


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class Tile(Enum):
    EMPTY = "."
    VERTICAL_SPLITTER = "|"
    HORIZONTAL_SPLITTER = "-"
    RIGHT_TILTED_MIRROR = "R"
    LEFT_TILTED_MIRROR = "L"


class LightBeamNode:
    def __init__(self, idx, last_dir, next_dir):
        self.idx = idx
        self.last_dir = last_dir
        self.next_dir = next_dir


def get_next_tile_idx(tile_idx, direction):
    dx, dy = direction.value
    return (tile_idx[0] + dx, tile_idx[1] + dy)


def simulate_light_beam(
    grid, start_pos=(0, 0), last_dir=Direction.LEFT, next_dir=Direction.RIGHT
):
    energized_tiles = set()
    queue = deque()

    # Initialize the light beam's starting position and direction.
    node = LightBeamNode(start_pos, last_dir, next_dir)
    queue.append(node)

    while queue:
        # Process the next node in the queue.
        node = queue.popleft()

        # Skip processing if the node is out of the grid's bounds.
        if (
            node.idx[0] < 0
            or node.idx[0] >= len(grid[0])
            or node.idx[1] < 0
            or node.idx[1] >= len(grid)
        ):
            continue

        # Skip processing if the tile in this direction has already been energized.
        if (node.idx, node.last_dir) in energized_tiles:
            continue
        else:
            energized_tiles.add((node.idx, node.last_dir))

        # Get the tile at the current node's position.
        tile = grid[node.idx[0]][node.idx[1]]

        # If the tile is empty, propagate the light beam in the same direction.
        if tile == Tile.EMPTY.value:
            queue.append(
                LightBeamNode(
                    get_next_tile_idx(node.idx, node.next_dir),
                    node.last_dir,
                    node.next_dir,
                )
            )

        # Handle interaction with vertical splitters.
        elif tile == Tile.VERTICAL_SPLITTER.value:
            # Continue in the same direction if moving vertically.
            if node.last_dir in [Direction.UP, Direction.DOWN]:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, node.next_dir),
                        node.last_dir,
                        node.next_dir,
                    )
                )

            # Split the beam in up and down directions if moving horizontally.
            else:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.UP),
                        Direction.DOWN,
                        Direction.UP,
                    )
                )
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.DOWN),
                        Direction.UP,
                        Direction.DOWN,
                    )
                )

        # Handle interaction with horizontal splitters.
        elif tile == Tile.HORIZONTAL_SPLITTER.value:
            # Continue in the same direction if moving horizontally.
            if node.last_dir in [Direction.LEFT, Direction.RIGHT]:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, node.next_dir),
                        node.last_dir,
                        node.next_dir,
                    )
                )

            # Split the beam in left and right directions if moving vertically.
            else:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.LEFT),
                        Direction.RIGHT,
                        Direction.LEFT,
                    )
                )
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.RIGHT),
                        Direction.LEFT,
                        Direction.RIGHT,
                    )
                )

        # Handle interaction with right-tilted mirrors.
        elif tile == Tile.RIGHT_TILTED_MIRROR.value:
            # Change direction based on the mirror's orientation and the beam's current direction.
            if node.last_dir == Direction.UP:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.LEFT),
                        Direction.RIGHT,
                        Direction.LEFT,
                    )
                )
            elif node.last_dir == Direction.RIGHT:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.DOWN),
                        Direction.UP,
                        Direction.DOWN,
                    )
                )
            elif node.last_dir == Direction.DOWN:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.RIGHT),
                        Direction.LEFT,
                        Direction.RIGHT,
                    )
                )
            elif node.last_dir == Direction.LEFT:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.UP),
                        Direction.DOWN,
                        Direction.UP,
                    )
                )

        # Handle interaction with left-tilted mirrors.
        elif tile == Tile.LEFT_TILTED_MIRROR.value:
            # Change direction based on the mirror's orientation and the beam's current direction.
            if node.last_dir == Direction.UP:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.RIGHT),
                        Direction.LEFT,
                        Direction.RIGHT,
                    )
                )
            elif node.last_dir == Direction.RIGHT:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.UP),
                        Direction.DOWN,
                        Direction.UP,
                    )
                )
            elif node.last_dir == Direction.DOWN:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.LEFT),
                        Direction.RIGHT,
                        Direction.LEFT,
                    )
                )
            elif node.last_dir == Direction.LEFT:
                queue.append(
                    LightBeamNode(
                        get_next_tile_idx(node.idx, Direction.DOWN),
                        Direction.UP,
                        Direction.DOWN,
                    )
                )

    # Create a new grid representation showing the energized tiles.
    new_grid = [
        [Tile.EMPTY.value for _ in range(len(grid[0]))] for _ in range(len(grid))
    ]

    # Mark energized tiles in the new grid.
    for tile, _ in energized_tiles:
        new_grid[tile[0]][tile[1]] = "#"

    return new_grid


def process_tile(grid, tile, last_dir, next_dir, record):
    updated_grid = simulate_light_beam(
        grid, start_pos=tile, last_dir=last_dir, next_dir=next_dir
    )
    record.append(sum(tile == "#" for row in updated_grid for tile in row))


def get_max_energized_tiles(grid):
    energized_tiles_record = []

    grid_corners = [
        (0, 0),
        (0, len(grid[0]) - 1),
        (len(grid) - 1, 0),
        (len(grid) - 1, len(grid[0]) - 1),
    ]

    directions = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]

    # Process corners
    for corner in grid_corners:
        for i in range(2):
            process_tile(
                grid,
                corner,
                directions[i * 2],
                directions[i * 2 + 1],
                energized_tiles_record,
            )

    # Process edges without corners
    for i in range(1, len(grid[0]) - 1):  # Top and bottom rows
        process_tile(grid, (0, i), Direction.UP, Direction.DOWN, energized_tiles_record)
        process_tile(
            grid,
            (len(grid) - 1, i),
            Direction.DOWN,
            Direction.UP,
            energized_tiles_record,
        )

    for i in range(1, len(grid) - 1):  # Left and right columns
        process_tile(
            grid, (i, 0), Direction.LEFT, Direction.RIGHT, energized_tiles_record
        )
        process_tile(
            grid,
            (i, len(grid[0]) - 1),
            Direction.RIGHT,
            Direction.LEFT,
            energized_tiles_record,
        )

    return max(energized_tiles_record)


def parse_input(input_str):
    grid = []
    for line in input_str.splitlines():
        grid.append(list(line))
    return grid


def part_one():
    with open("day_16/input.txt", "r") as f:
        input_str = f.read()
    grid = parse_input(input_str)
    updated_grid = simulate_light_beam(grid)
    num_of_energized_tiles = sum(tile == "#" for row in updated_grid for tile in row)
    print(f"❗️ Number of energized tiles: {num_of_energized_tiles}")


def part_two():
    with open("day_16/input.txt", "r") as f:
        input_str = f.read()
    grid = parse_input(input_str)
    maximum_energized_tiles = get_max_energized_tiles(grid)
    print(f"❗️❗️ Number of energized tiles: {maximum_energized_tiles}")


def test_get_max_energized_tiles():
    input_str = """.|...L....
|.-.L.....
.....|-...
........|.
..........
.........L
....R.LL..
.-.-R..|..
.|....-|.L
..RR.|...."""
    grid = parse_input(input_str)
    maximum_energized_tiles = get_max_energized_tiles(grid)
    assert maximum_energized_tiles == 51, f"Expected 51, got {maximum_energized_tiles}"
    print("✅ test_get_max_energized_tiles passed")


def test_get_energized_tiles():
    input_str = """.|...L....
|.-.L.....
.....|-...
........|.
..........
.........L
....R.LL..
.-.-R..|..
.|....-|.L
..RR.|...."""

    grid = parse_input(input_str)
    updated_grid = simulate_light_beam(grid)
    num_of_energized_tiles = sum(tile == "#" for row in updated_grid for tile in row)
    assert num_of_energized_tiles == 46, f"Expected 46, got {num_of_energized_tiles}"
    print("✅ test_get_energized_tiles passed")


if __name__ == "__main__":
    test_get_energized_tiles()
    part_one()

    test_get_max_energized_tiles()
    part_two()
