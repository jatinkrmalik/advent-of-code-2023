# Day 18: Lavaduct Lagoon

from enum import Enum


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


dig_plan_to_direction = {
    "U": Direction.UP,
    "D": Direction.DOWN,
    "L": Direction.LEFT,
    "R": Direction.RIGHT,
}


class TrenchLine:
    hex_to_directions = {
        "0": Direction.RIGHT,
        "1": Direction.DOWN,
        "2": Direction.LEFT,
        "3": Direction.UP,
    }

    def __init__(self, start_x, start_y, direction, distance):
        self.start_x = start_x
        self.start_y = start_y
        self.direction = direction
        self.distance = distance
        self.end_x, self.end_y = self.calculate_end_coordinates()

    def calculate_end_coordinates(self):
        return (
            self.start_x + self.direction.value[0] * self.distance,
            self.start_y + self.direction.value[1] * self.distance,
        )

    def __repr__(self):
        return f"({self.start_x}, {self.start_y}) -> ({self.end_x}, {self.end_y})"

    @staticmethod
    def from_hex_code(start_x, start_y, hex_code):
        hex_code = hex_code[1:-1][1:]
        dig_distance = int(hex_code[:-1], 16)
        dig_direction_hex = hex_code[-1]
        dig_direction = TrenchLine.hex_to_directions[dig_direction_hex]
        return TrenchLine(start_x, start_y, dig_direction, dig_distance)


class Lagoon:
    DEPTH = 1

    @staticmethod
    def get_trench_volume(trench_lines):
        return sum(line.distance for line in trench_lines) * Lagoon.DEPTH

    @staticmethod
    def get_lagoon_volume(trench_lines):
        polygon_points = [(line.start_x, line.start_y) for line in trench_lines] + [
            (trench_lines[-1].end_x, trench_lines[-1].end_y)
        ]
        lagoon_area = abs(
            sum(
                polygon_points[i][0] * polygon_points[(i + 1) % len(polygon_points)][1]
                - polygon_points[(i + 1) % len(polygon_points)][0]
                * polygon_points[i][1]
                for i in range(len(polygon_points))
            )
            / 2.0
        )
        return int(lagoon_area + Lagoon.get_trench_volume(trench_lines) // 2 + 1) * Lagoon.DEPTH


def dig_trench_simple(dig_plan):
    start_x, start_y = 0, 0
    trench_lines = []

    for direction_key, distance, _ in dig_plan:
        direction = dig_plan_to_direction[direction_key]
        trench_line = TrenchLine(start_x, start_y, direction, int(distance))
        trench_lines.append(trench_line)
        start_x, start_y = trench_line.end_x, trench_line.end_y

    return trench_lines


def dig_trench_hex(dig_plan):
    start_x, start_y = 0, 0
    trench_lines = []

    for _, _, hex_code in dig_plan:
        trench_line = TrenchLine.from_hex_code(start_x, start_y, hex_code)
        trench_lines.append(trench_line)
        start_x, start_y = trench_line.end_x, trench_line.end_y

    return trench_lines


def test_lavaduct_lagoon():
    input_str = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

    dig_plan = [line.split() for line in input_str.split("\n")]
    trench_lines = dig_trench_simple(dig_plan)
    trench_volume = Lagoon.get_trench_volume(trench_lines)
    assert trench_volume == 38, f"Expected 38, got {trench_volume}"
    print("✅ get_trench_volume passed")

    lagoon_volume = Lagoon.get_lagoon_volume(trench_lines)
    assert lagoon_volume == 62, f"Expected 62, got {lagoon_volume}"
    print("✅ get_lagoon_volume passed")


def test_lavaduct_lagoon_hex():
    input_str = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""

    dig_plan = [line.split() for line in input_str.split("\n")]
    trench_lines = dig_trench_hex(dig_plan)
    trench_volume = Lagoon.get_trench_volume(trench_lines)
    assert trench_volume == 6405262, f"Expected 6405262, got {trench_volume}"
    print("✅ get_trench_volume passed")

    lagoon_volume = Lagoon.get_lagoon_volume(trench_lines)
    assert lagoon_volume == 952408144115, f"Expected 952408144115, got {lagoon_volume}"
    print("✅ get_lagoon_volume passed")


def part_one():
    with open("day_18/input.txt", "r") as f:
        dig_plan = [line.split() for line in f.readlines()]

    trench_lines = dig_trench_simple(dig_plan)
    lagoon_volume = Lagoon.get_lagoon_volume(trench_lines)
    print(f"❗️ Our lagoon can hold {lagoon_volume} m^3 of lava!")


def part_two():
    with open("day_18/input.txt", "r") as f:
        dig_plan = [line.split() for line in f.readlines()]

    trench_lines = dig_trench_hex(dig_plan)
    lagoon_volume = Lagoon.get_lagoon_volume(trench_lines)
    print(f"❗️❗️ Our lagoon can actually hold {lagoon_volume} m^3 of lava!")


if __name__ == "__main__":
    test_lavaduct_lagoon()
    part_one()

    test_lavaduct_lagoon_hex()
    part_two()
