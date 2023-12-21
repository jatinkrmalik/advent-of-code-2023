# Day 14 - Parabolic Reflector Dish

from enum import Enum


class TiltDirection(Enum):
    North = "NORTH"
    South = "SOUTH"
    East = "EAST"
    West = "WEST"


class Tile(Enum):
    Empty = "."
    CubeRock = "#"
    RoundRock = "O"


def tilt_platform(platform_state, direction):
    rows, cols = len(platform_state), len(platform_state[0])
    delta = {
        TiltDirection.North: (0, -1),
        TiltDirection.South: (0, 1),
        TiltDirection.East: (1, 0),
        TiltDirection.West: (-1, 0)
    }[direction]

    def is_valid_position(row, col):
        return 0 <= row < rows and 0 <= col < cols

    def move_rock(start_row, start_col):
        row, col = start_row, start_col
        while is_valid_position(row + delta[1], col + delta[0]) and \
                platform_state[row + delta[1]][col + delta[0]] == Tile.Empty.value:
            platform_state[row][col] = Tile.Empty.value
            row, col = row + delta[1], col + delta[0]
            platform_state[row][col] = Tile.RoundRock.value

    if direction in [TiltDirection.North, TiltDirection.West]:
        range_func = range
    else:
        range_func = lambda start, end: range(end - 1, start - 1, -1)

    for i in range_func(0, rows):
        for j in range_func(0, cols):
            if platform_state[i][j] == Tile.RoundRock.value:
                move_rock(i, j)

    return platform_state


def tilt_platform_cycle(platform_state, num_cycles=1):    
    platform_cache = {}  # Cache for storing seen platform states
    cycle_patterns = []  # List to store unique states forming a cycle
    cycle_start_point = None


    for idx in range(1, num_cycles+1):
        # Tilt platform in all directions
        for direction in [TiltDirection.North, TiltDirection.West, TiltDirection.South, TiltDirection.East]:
            platform_state = tilt_platform(platform_state, direction)

        # Generate a key for the current state
        platform_state_key = "\n".join([" ".join(map(str, row)) for row in platform_state])
       
        # Check if the current state has been seen before
        if platform_state_key in platform_cache:
            if cycle_start_point is None:
                cycle_start_point = platform_cache[platform_state_key]
                cycle_patterns.append(platform_state_key)
                continue

            # Start of the cycle found, calculate the index in the cycle pattern
            if platform_state_key == cycle_patterns[0]:
                cycle_length = len(cycle_patterns)
                cycle_index = (num_cycles - cycle_start_point) % cycle_length
                return [list(row) for row in cycle_patterns[cycle_index].split("\n")]

            # New state in the cycle
            if platform_state_key not in cycle_patterns:
                cycle_patterns.append(platform_state_key)
            continue

        # Store the new state in the cache
        platform_cache[platform_state_key] = idx
        if cycle_start_point is not None and platform_state_key not in cycle_patterns:
            cycle_patterns.append(platform_state_key)

    return platform_state


def calculate_load_on_north_beam(tilted_platform_state):
    return sum((len(tilted_platform_state) - i) * row.count(Tile.RoundRock.value)
               for i, row in enumerate(tilted_platform_state))


def part_one():
    with open("day_14/input.txt") as f:
        platform_state = f.read()

    # split the platform state into rows
    platform_state = [list(row) for row in platform_state.split("\n")]

    tilted_platform_state = tilt_platform(platform_state, TiltDirection.North)
    total_load = calculate_load_on_north_beam(tilted_platform_state)
    print(f"❗️ Total load on the north beam is {total_load}")


def part_two():
    with open("day_14/input.txt") as f:
        platform_state = f.read()

    # split the platform state into rows
    platform_state = [list(row) for row in platform_state.split("\n")]

    tilted_platform_state = tilt_platform_cycle(platform_state, 1000000000)
    total_load = calculate_load_on_north_beam(tilted_platform_state)
    print(f"‼️ Total load on the north beam after 1000000000 cycles is {total_load}")


def test_tilt_platform_cycle():
    platform_state_og = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

    expected_platform_state_with_1_cycle = """.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""

    expected_platform_state_with_2_cycles = """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O"""

    expected_platform_state_with_3_cycles = """.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""

    # split the platform state into rows
    platform_state = [list(row) for row in platform_state_og.split("\n")]
    expected_platform_state_with_1_cycle = [
        list(row) for row in expected_platform_state_with_1_cycle.split("\n")
    ]
    tilted_platform_state = tilt_platform_cycle(platform_state, 1)
    assert (
        tilted_platform_state == expected_platform_state_with_1_cycle
    ), f"Expected {expected_platform_state_with_1_cycle}, got {tilted_platform_state}"
    print("✅ tilt_platform_cycle with 1 cycle passed")

    # reseting platform_state
    platform_state = [list(row) for row in platform_state_og.split("\n")]
    expected_platform_state_with_2_cycles = [
        list(row) for row in expected_platform_state_with_2_cycles.split("\n")
    ]
    tilted_platform_state = tilt_platform_cycle(platform_state, 2)
    assert (
        tilted_platform_state == expected_platform_state_with_2_cycles
    ), f"Expected {expected_platform_state_with_2_cycles}, got {tilted_platform_state}"
    print("✅ tilt_platform_cycle with 2 cycles passed")

    # reseting platform_state
    platform_state = [list(row) for row in platform_state_og.split("\n")]
    expected_platform_state_with_3_cycles = [
        list(row) for row in expected_platform_state_with_3_cycles.split("\n")
    ]
    tilted_platform_state = tilt_platform_cycle(platform_state, 3)
    assert (
        tilted_platform_state == expected_platform_state_with_3_cycles
    ), f"Expected {expected_platform_state_with_3_cycles}, got {tilted_platform_state}"
    print("✅ tilt_platform_cycle with 3 cycles passed")


def test_tilt_platform():
    platform_state = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

    expected_platform_state = """OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#...."""
    # split the platform state into rows
    platform_state = [list(row) for row in platform_state.split("\n")]
    tilted_platform_state = tilt_platform(platform_state, TiltDirection.North)
    assert tilted_platform_state == [
        list(row) for row in expected_platform_state.split("\n")
    ], f"Expected {expected_platform_state}, got {tilted_platform_state}"
    print("✅ tilt_platform passed")


def test_calculate_load_on_north_beam():
    platform_state = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
    # split the platform state into rows
    platform_state = [list(row) for row in platform_state.split("\n")]
    tilted_platform_state = tilt_platform(platform_state, TiltDirection.North)
    total_load = calculate_load_on_north_beam(tilted_platform_state)
    assert total_load == 136, f"Expected 136, got {total_load}"
    print("✅ test_calculate_load_on_north_beam passed")


def test_calculate_load_on_north_beam_1000000000_cycles():
    platform_state = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
    # split the platform state into rows
    platform_state = [list(row) for row in platform_state.split("\n")]
    tilted_platform_state = tilt_platform_cycle(platform_state, 1000000000)
    total_load = calculate_load_on_north_beam(tilted_platform_state)
    assert total_load == 64, f"Expected 64, got {total_load}"
    print("✅ test_calculate_load_on_north_beam_1000000000_cycles passed")


if __name__ == "__main__":
    test_tilt_platform()
    test_calculate_load_on_north_beam()
    part_one()

    test_tilt_platform_cycle()
    test_calculate_load_on_north_beam_1000000000_cycles()
    part_two()
