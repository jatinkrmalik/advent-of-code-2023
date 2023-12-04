# --- Day 3: Gear Ratios ---

class EngineSchematicAnalyzer:
    DIRECTIONS = [
        (-1, -1), # Top-left
        (-1, 0),  # Up
        (-1, 1),  # Top-right
        (0, -1),  # Left
        (0, 1),   # Right
        (1, -1),  # Bottom-left
        (1, 0),   # Down
        (1, 1)    # Bottom-right
    ]

    def __init__(self, schematic):
        self.schematic = [list(line) for line in schematic.split('\n')]
        self.processed_locations = set()

    def calculate_sum_of_part_numbers(self):
        total_sum = 0
        for i, row in enumerate(self.schematic):
            j = 0
            while j < len(row):
                if row[j].isdigit() and (i, j) not in self.processed_locations:
                    part_number = self._get_full_part_number(i, j)
                    self.processed_locations.update(
                        (i, col_index) for col_index in range(j, j + len(str(part_number)))
                    )

                    if any(self._is_adjacent_to_symbol(i, col_index) for col_index in range(j, j + len(str(part_number)))):
                        total_sum += part_number
                    j += len(str(part_number)) - 1
                j += 1
            
        return total_sum
    
    def calculate_sum_of_all_gear_ratios(self):
        total_sum = 0
        for i, row in enumerate(self.schematic):
            for j, char in enumerate(row):
                total_sum += self._get_gear_ratio(i, j) if char == '*' else 0
        
        return total_sum

    def _get_gear_ratio(self, row, col):
        adjacent_numbers = []
        for dx, dy in self.DIRECTIONS:
            adjacent_row, adjacent_col = row + dx, col + dy
            if 0 <= adjacent_row < len(self.schematic) and 0 <= adjacent_col < len(self.schematic[adjacent_row]):
                if self.schematic[adjacent_row][adjacent_col].isdigit():
                    part_number = self._get_full_part_number(adjacent_row, adjacent_col)
                    if part_number not in adjacent_numbers:
                        adjacent_numbers.append(part_number)

        if len(adjacent_numbers) == 2:
            return adjacent_numbers[0] * adjacent_numbers[1]
        return 0

    def _get_full_part_number(self, row, col):
        # start with the digit at (row, col)
        number_str = self.schematic[row][col]

        # fan out to the left
        left_col = col - 1
        while left_col >= 0 and self.schematic[row][left_col].isdigit():
            number_str = self.schematic[row][left_col] + number_str
            left_col -= 1

        # fan out to the right
        right_col = col + 1
        while right_col < len(self.schematic[row]) and self.schematic[row][right_col].isdigit():
            number_str += self.schematic[row][right_col]
            right_col += 1

        return int(number_str)

    def _is_valid_symbol(self, char):
        return not (char.isdigit() or char == '.')

    def _is_adjacent_to_symbol(self, row, col):
        for dx, dy in self.DIRECTIONS:
            if 0 <= row + dx < len(self.schematic) and 0 <= col + dy < len(self.schematic[row + dx]):
                if self._is_valid_symbol(self.schematic[row + dx][col + dy]):
                    return True
        return False

# solves the Part 1 of the problem
def part_1():
    with open("day_3/input.txt") as file:
        engine_schematic = file.read()

    analyzer = EngineSchematicAnalyzer(engine_schematic)
    total_sum = analyzer.calculate_sum_of_part_numbers()
    print(f"Sum of part numbers is {total_sum}")

# solves the Part 2 of the problem
def part_2():
    with open("day_3/input.txt") as file:
        engine_schematic = file.read()
    
    analyzer = EngineSchematicAnalyzer(engine_schematic)
    total_sum = analyzer.calculate_sum_of_all_gear_ratios()
    print(f"Sum of all gear ratios is {total_sum}")

def test_sum_of_part_numbers():
    engine_schematic = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

    analyzer = EngineSchematicAnalyzer(engine_schematic)
    calculated_sum = analyzer.calculate_sum_of_part_numbers()
    assert calculated_sum == 4361, f"sum of part numbers is {calculated_sum}"
    print("test_sum_of_part_numbers passed successfully!")

def test_sum_of_all_gear_ratios():
    engine_schematic = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
    analyzer = EngineSchematicAnalyzer(engine_schematic)
    calculated_sum = analyzer.calculate_sum_of_all_gear_ratios()
    assert calculated_sum == 467835, f"sum of all gear ratios is {calculated_sum}"
    print("test_sum_of_all_gear_ratios passed successfully!")

if __name__ == "__main__":
    # base test cases
    test_sum_of_part_numbers()
    test_sum_of_all_gear_ratios()

    # run the main function using the input file
    part_1() 
    part_2()

# I know there's still some scope of improvement in the code above
# that I might pick later, but it's 1AM, I want to sleep as I have 
# work tomorrow! Feel free to raise a PR. 😅