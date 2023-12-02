# --- Day 2: Cube Conundrum ---
# --- Part Two ---

from functools import reduce
from operator import mul


class CubeGameAnalyzer:
    def __init__(self, games, max_cubes=None):
        self.games = games
        self.max_cubes = max_cubes

    def sum_of_possible_game_ids(self):
        sum_ids = 0
        for game in self.games:
            try:
                game_id, sequences = game.split(": ")
                if self._is_game_possible(sequences):
                    sum_ids += int(game_id.split()[1])
            except ValueError as e:
                print(f"Error processing game data: {e}")
        return sum_ids

    def sum_of_power_of_games(self):
        sum_power_of_games = 0
        for game in self.games:
            game_sets = game.split(": ")[1].split("; ")
            min_cubes_required = {"red": 0, "green": 0, "blue": 0}

            for cubes in game_sets:
                for count, color in map(str.split, cubes.split(", ")):
                    min_cubes_required[color] = max(
                        int(count), min_cubes_required[color]
                    )

            game_power = reduce(mul, min_cubes_required.values(), 1)
            sum_power_of_games += game_power

        return sum_power_of_games

    def _is_game_possible(self, game_sequence):
        sequences = game_sequence.split(";")
        for sequence in sequences:
            sequence = sequence.strip()
            if not self._is_sequence_possible(sequence):
                return False
        return True

    def _is_sequence_possible(self, sequence):
        cubes = sequence.split(",")
        for cube in cubes:
            count, color = cube.strip().split()
            if int(count) > self.max_cubes[color]:
                return False
        return True


def main():
    # read games from the input file
    with open("day_2/input.txt") as f:
        games = f.readlines()

    analyzer = CubeGameAnalyzer(games)
    print(analyzer.sum_of_power_of_games())


def test_cube_game_analyzer():
    games = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]

    analyzer = CubeGameAnalyzer(games)
    sum_of_power_of_games = analyzer.sum_of_power_of_games()

    assert (
        sum_of_power_of_games == 2286
    ), f"Test failed: Expected 2286, got {sum_of_power_of_games}"
    print(f"Test passed: Sum of Power of Games is {sum_of_power_of_games}")


if __name__ == "__main__":
    # run the test function
    test_cube_game_analyzer()

    # execute the main function
    main()
