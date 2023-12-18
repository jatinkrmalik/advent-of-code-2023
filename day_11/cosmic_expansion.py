# Day 11: Cosmic Expansion

class CosmicGrid:
    def __init__(self, space_grid):
        # Initialize the cosmic grid with the provided space grid
        self.space_grid = space_grid
        self.grid_height = len(space_grid)
        self.grid_width = len(space_grid[0])
        # Find rows and columns that are entirely empty
        self.empty_rows = self._find_empty_rows()
        self.empty_columns = self._find_empty_columns()
        # Locate all galaxies within the grid
        self.galaxy_positions = self._find_galaxy_positions()

    def _find_empty_rows(self):
        # Identify rows that contain only empty space
        empty_rows = set()
        for row in range(self.grid_height):
            if all(cell == '.' for cell in self.space_grid[row]):
                empty_rows.add(row)
        return empty_rows

    def _find_empty_columns(self):
        # Identify columns that contain only empty space
        empty_columns = set()
        for col in range(self.grid_width):
            if all(self.space_grid[row][col] == '.' for row in range(self.grid_height)):
                empty_columns.add(col)
        return empty_columns

    def _find_galaxy_positions(self):
        # Record the positions of all galaxies in the grid
        galaxy_positions = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.space_grid[row][col] == '#':
                    galaxy_positions.append((row, col))
        return galaxy_positions

    def find_shortest_distance(self, galaxy1, galaxy2, expansion_factor):
        # Calculate the shortest distance between two galaxies, factoring in cosmic expansion
        row_distance = 0
        for r in range(min(galaxy1[0], galaxy2[0]), max(galaxy1[0], galaxy2[0]) + 1):
            if r in self.empty_rows:
                row_distance += 1

        col_distance = 0
        for c in range(min(galaxy1[1], galaxy2[1]), max(galaxy1[1], galaxy2[1]) + 1):
            if c in self.empty_columns:
                col_distance += 1

        # Expanded distance is calculated by multiplying empty distances by the expansion factor
        # Direct distance is the straight line distance, not through empty space
        expanded_row_distance = row_distance * expansion_factor
        expanded_col_distance = col_distance * expansion_factor
        direct_distance = abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])

        return expanded_row_distance + expanded_col_distance + direct_distance - row_distance - col_distance

    def sum_of_shortest_paths(self, expansion_factor):
        # Sum the shortest paths between all pairs of galaxies
        total_distance = 0
        for i, galaxy1 in enumerate(self.galaxy_positions):
            for galaxy2 in self.galaxy_positions[i + 1:]:
                total_distance += self.find_shortest_distance(galaxy1, galaxy2, expansion_factor)
        return total_distance



def part_one():
    with open("day_11/input.txt") as f:
        space_map = f.read().splitlines()

    cosmic_grid = CosmicGrid(space_map)
    sum = cosmic_grid.sum_of_shortest_paths(expansion_factor=2)
    print(
        f"❗️ Sum of the lengths of the shortest path between every pair of galaxies for expansion_factor=2: {sum}"
    )


def part_two():
    with open("day_11/input.txt") as f:
        space_map = f.read().splitlines()

    cosmic_grid = CosmicGrid(space_map)
    sum = cosmic_grid.sum_of_shortest_paths(expansion_factor=1000000)
    print(
        f"‼️ Sum of the lengths of the shortest path between every pair of galaxies for expansion_factor=1000000: {sum}"
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
    cosmic_grid = CosmicGrid(space_map.splitlines())
    # part one
    sum = cosmic_grid.sum_of_shortest_paths(expansion_factor=2)
    assert sum == 374, f"Expected 374, got {sum}"
    print("✅ Passed test_analyze_observation() for expansion_factor=2")

    # part two
    sum = cosmic_grid.sum_of_shortest_paths(expansion_factor=10)
    assert sum == 1030, f"Expected 1030, got {sum}"
    print("✅ Passed test_analyze_observation() for expansion_factor=10")

    sum = cosmic_grid.sum_of_shortest_paths(expansion_factor=100)
    assert sum == 8410, f"Expected 8410, got {sum}"
    print("✅ Passed test_analyze_observation() for expansion_factor=100")


if __name__ == "__main__":
    test_analyze_space()
    part_one()
    part_two()
