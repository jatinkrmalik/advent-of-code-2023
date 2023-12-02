# --- Day 2: Cube Conundrum ---
# --- Part One ---


class CubeGameAnalyzer:
    def __init__(self, max_cubes):
        self.max_cubes = max_cubes

    def sum_of_possible_game_ids(self, games):
        sum_ids = 0
        for game in games:
            try:
                game_id, sequences = game.split(": ")
                if self._is_game_possible(sequences):
                    sum_ids += int(game_id.split()[1])
            except ValueError as e:
                print(f"Error processing game data: {e}")
        return sum_ids

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

    # calculate and display the sum of possible game IDs
    max_cubes = {"red": 12, "green": 13, "blue": 14}
    analyzer = CubeGameAnalyzer(max_cubes)
    print(analyzer.sum_of_possible_game_ids(games))


def test_cube_game_analyzer():
    games = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]
    max_cubes = {"red": 12, "green": 13, "blue": 14}

    analyzer = CubeGameAnalyzer(max_cubes)
    sum_of_ids = analyzer.sum_of_possible_game_ids(games)

    assert sum_of_ids == 8, f"Test failed: Expected 8, got {sum_of_ids}"
    print(f"Test passed: Sum of IDs is {sum_of_ids}")


if __name__ == "__main__":
    # run the test function
    test_cube_game_analyzer()

    # execute the main function
    main()
