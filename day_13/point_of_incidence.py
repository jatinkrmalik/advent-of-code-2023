# Day 13 - Point of Incidence

from enum import Enum
import itertools


class Mode(Enum):
    ROW = "row"
    COLUMN = "column"


class MirrorPatternAnalyzer:
    def __init__(self, pattern):
        self.pattern = [list(row) for row in pattern.strip().split("\n")]

    @staticmethod
    def flip_char(char):
        return "#" if char == "." else "."

    def is_perfect_reflection(self, index, mode):
        if mode == Mode.ROW:
            prev, next = index - 1, index
            while prev >= 0 and next < len(self.pattern):
                if self.pattern[prev] != self.pattern[next]:
                    return False
                prev -= 1
                next += 1
            return True

        elif mode == Mode.COLUMN:
            prev, next = index - 1, index
            while prev >= 0 and next < len(self.pattern[0]):
                if any(
                    self.pattern[row][prev] != self.pattern[row][next]
                    for row in range(len(self.pattern))
                ):
                    return False
                prev -= 1
                next += 1
            return True

        raise ValueError("Invalid mode")

    def find_point_of_reflection(self, mode):
        range_to_check = range(
            1, len(self.pattern) if mode == Mode.ROW else len(self.pattern[0])
        )
        for i in range_to_check:
            if self.is_perfect_reflection(i, mode):
                return i
        return None

    def try_fix_smudge_and_find_reflection(
        self, original_reflection_point, original_mode
    ):
        for i in range(len(self.pattern)):
            for j in range(len(self.pattern[i])):
                self.pattern[i][j] = MirrorPatternAnalyzer.flip_char(self.pattern[i][j])
                for mode in [Mode.ROW, Mode.COLUMN]:
                    new_reflection_point = self.find_point_of_reflection(mode)
                    if new_reflection_point and (new_reflection_point, mode) != (
                        original_reflection_point,
                        original_mode,
                    ):
                        return new_reflection_point, mode
                self.pattern[i][j] = MirrorPatternAnalyzer.flip_char(self.pattern[i][j])
        return original_reflection_point, original_mode

    def analyze(self, with_smudge=False):
        for mode in [Mode.ROW, Mode.COLUMN]:
            reflection_point = self.find_point_of_reflection(mode)
            if reflection_point is not None:
                if with_smudge:
                    (
                        new_reflection_point,
                        new_mode,
                    ) = self.try_fix_smudge_and_find_reflection(reflection_point, mode)
                    if new_mode == Mode.ROW:
                        return new_reflection_point * 100
                    else:
                        return new_reflection_point
                else:
                    return (
                        reflection_point * 100 if mode == Mode.ROW else reflection_point
                    )
        raise Exception("No valid reflection line found")


def summarize_patterns(patterns, with_smudges=False):
    total_sum = 0
    for i, pattern in enumerate(patterns.split("\n\n")):
        analyzer = MirrorPatternAnalyzer(pattern)
        total_sum += analyzer.analyze(with_smudge=with_smudges)
    return total_sum


def part_one():
    with open("day_13/input.txt", "r") as f:
        patterns = f.read()
    sum = summarize_patterns(patterns)

    print(f"❗️ Summarizing all patterns in Part 1: {sum}")


def test_summarize_patterns():
    patterns = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
    sum = summarize_patterns(patterns)
    assert sum == 405, f"Expected 405, got {sum}"
    print("✅ summarize_pattern passed")


def part_two():
    with open("day_13/input.txt", "r") as f:
        patterns = f.read()
    sum = summarize_patterns(patterns, with_smudges=True)
    print(f"‼️ Summarizing all patterns in Part 2: {sum}")


def test_summarize_patterns_with_smudges():
    patterns = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

    sum = summarize_patterns(patterns, with_smudges=True)
    assert sum == 400, f"Expected 400, got {sum}"
    print("✅ summarize_pattern_with_smudges passed")


if __name__ == "__main__":
    test_summarize_patterns()
    part_one()

    test_summarize_patterns_with_smudges()
    part_two()
