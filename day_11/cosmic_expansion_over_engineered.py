# Day 11: Cosmic Expansion

from enum import Enum
import heapq


EMPTY_SPACE = "."
GALAXY = "#"
DISTANCE_MAP = {}


class Direction(Enum):
    RIGHT = (0, 1)
    LEFT = (0, -1)
    DOWN = (1, 0)
    UP = (-1, 0)


def calculate_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance


def get_adjacent_galaxies(space_map, galaxy):
    adjacent_galaxies = []
    for direction in Direction:
        i, j = galaxy[0] + direction.value[0], galaxy[1] + direction.value[1]
        if 0 <= i < len(space_map) and 0 <= j < len(space_map[0]):
            adjacent_galaxies.append((i, j))
    return adjacent_galaxies


def find_shortest_path(space_map, start_galaxy, end_galaxy):
    galaxies_to_visit = []
    heapq.heappush(galaxies_to_visit, (0, start_galaxy))
    previous_galaxy = {}
    cost_to_reach = {start_galaxy: 0}
    estimated_total_cost = {start_galaxy: calculate_distance(start_galaxy, end_galaxy)}

    while galaxies_to_visit:
        current_galaxy = heapq.heappop(galaxies_to_visit)[1]

        if current_galaxy == end_galaxy:
            return cost_to_reach[
                current_galaxy
            ]  # Return the cost to reach the end galaxy

        for adjacent_galaxy in get_adjacent_galaxies(space_map, current_galaxy):
            tentative_cost = cost_to_reach[current_galaxy] + 1  # assuming uniform cost
            if (
                adjacent_galaxy not in cost_to_reach
                or tentative_cost < cost_to_reach[adjacent_galaxy]
            ):
                previous_galaxy[adjacent_galaxy] = current_galaxy
                cost_to_reach[adjacent_galaxy] = tentative_cost
                estimated_total_cost[
                    adjacent_galaxy
                ] = tentative_cost + calculate_distance(adjacent_galaxy, end_galaxy)
                heapq.heappush(
                    galaxies_to_visit,
                    (estimated_total_cost[adjacent_galaxy], adjacent_galaxy),
                )

    raise Exception("No path found between the two galaxies")


def expand_space_map(space_map):
    empty_rows, empty_cols = [], []

    for i, row in enumerate(space_map):
        if GALAXY not in row:
            empty_rows.append(i)

    for i, col in enumerate(space_map[0]):
        if GALAXY not in [row[i] for row in space_map]:
            empty_cols.append(i)

    mod_count = 0
    for i in empty_rows:
        space_map.insert(i + mod_count, EMPTY_SPACE * len(space_map[i]))
        mod_count += 1

    mod_count = 0
    for i in empty_cols:
        for j, row in enumerate(space_map):
            space_map[j] = row[: i + mod_count] + EMPTY_SPACE + row[i + mod_count :]
        mod_count += 1

    return space_map


def find_shortest_distance(galaxy1, galaxy2, space_map):
    print(f"Finding shortest distance between {galaxy1} and {galaxy2}")

    distance = DISTANCE_MAP.get(galaxy1, {}).get(galaxy2) or DISTANCE_MAP.get(
        galaxy2, {}
    ).get(galaxy1)
    if distance:
        return distance

    distance = find_shortest_path(space_map, galaxy1, galaxy2)  # Use A* for pathfinding

    if galaxy1 not in DISTANCE_MAP:
        DISTANCE_MAP[galaxy1] = {}
    DISTANCE_MAP[galaxy1][galaxy2] = distance
    return distance


def find_all_galaxies(space_map):
    galaxies = []
    for i, row in enumerate(space_map):
        for j, col in enumerate(row):
            if col == GALAXY:
                galaxies.append((i, j))
    return galaxies


def analyze_space(space_map):
    expanded_space_map = expand_space_map(space_map)
    print(
        f"Expanded space map is {len(expanded_space_map)} x {len(expanded_space_map[0])}"
    )
    galaxies_locations = find_all_galaxies(expanded_space_map)
    print(f"Number of galaxies: {len(galaxies_locations)}")

    for galaxy1 in galaxies_locations:
        for galaxy2 in galaxies_locations:
            if galaxy1 != galaxy2:
                find_shortest_distance(galaxy1, galaxy2, expanded_space_map)

    sum = 0
    for k, v in DISTANCE_MAP.items():
        for k1, v1 in v.items():
            sum += v1

    return sum


def part_one():
    with open("day_11/input.txt") as f:
        space_map = f.read().splitlines()
    sum = analyze_space(space_map)
    print(
        f"❗️ Sum of the lengths of the shortest path between every pair of galaxies: {sum}"
    )


def test_analyze_space():
    space_map = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

    sum = analyze_space(space_map.splitlines())
    assert sum == 374, f"Expected 374, got {sum}"
    print("✅ Passed test_analyze_observation()")


if __name__ == "__main__":
    test_analyze_space()
    # part_one()
