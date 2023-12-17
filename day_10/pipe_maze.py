# -- Day 10: Pipe Maze ---

from enum import Enum


class Direction(Enum):
    """
    Enum representing cardinal directions with their grid movements.
    """

    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)


REVERSE_DIRECTION_MAP = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}

PIPE_MOVEMENT_OPTIONS = {
    "|": [Direction.NORTH, Direction.SOUTH],
    "-": [Direction.EAST, Direction.WEST],
    "L": [Direction.NORTH, Direction.EAST],
    "J": [Direction.NORTH, Direction.WEST],
    "7": [Direction.SOUTH, Direction.WEST],
    "F": [Direction.SOUTH, Direction.EAST],
    "S": [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST],
}


class Maze:
    def __init__(self, input_string):
        """
        Initialize the Maze with a string representation.
        :param input_string: Multiline string representing the maze.
        """
        self.maze = [list(line) for line in input_string.splitlines()]

    def find_animal_start(self):
        """
        Find the starting position of the animal marked by 'S' in the maze.
        :return: Tuple (x, y) as the starting position.
        """
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if cell == "S":
                    return (i, j)


class MazeSolver:
    def __init__(self, maze):
        """
        Initialize the MazeSolver with the maze.
        :param maze: 2D list representing the maze.
        """
        self.maze = maze

    def find_loop(self, start):
        """
        Find the loop in the maze starting from the given position.
        :param start: Tuple (x, y) as the starting position.
        :return: List of tuples representing the loop path.
        """
        stack = [start]
        visited = {start}
        path_tracker = {start: None}

        while stack:
            x, y = stack.pop()
            for direction in PIPE_MOVEMENT_OPTIONS[self.maze[x][y]]:
                nx, ny = x + direction.value[0], y + direction.value[1]
                if self.can_move(x, y, nx, ny, direction):
                    if (nx, ny) not in visited:
                        self.update_stack_and_visited(
                            stack, visited, path_tracker, x, y, nx, ny
                        )
                        break
                    elif path_tracker[(x, y)] != (nx, ny):
                        return self.construct_loop(path_tracker, x, y, nx, ny)
        raise ValueError("No loop found")

    def can_move(self, x, y, nx, ny, direction):
        """
        Check if movement is possible in the maze from (x, y) to (nx, ny).
        :param x, y: Current position coordinates.
        :param nx, ny: Next position coordinates.
        :param direction: Direction of movement.
        :return: Boolean indicating if movement is possible.
        """
        return (
            0 <= nx < len(self.maze)
            and 0 <= ny < len(self.maze[0])
            and self.maze[nx][ny] in PIPE_MOVEMENT_OPTIONS
            and REVERSE_DIRECTION_MAP[direction]
            in PIPE_MOVEMENT_OPTIONS[self.maze[nx][ny]]
        )

    def update_stack_and_visited(self, stack, visited, path_tracker, x, y, nx, ny):
        """
        Update the stack, visited set, and path tracker for the next move.
        :param stack: List representing the stack of positions to explore.
        :param visited: Set of visited positions.
        :param path_tracker: Dictionary tracking the path taken.
        :param x, y: Current position coordinates.
        :param nx, ny: Next position coordinates.
        """
        stack.append((nx, ny))
        visited.add((nx, ny))
        path_tracker[(nx, ny)] = (x, y)

    def construct_loop(self, path_tracker, x, y, nx, ny):
        """
        Construct the loop path when a loop is detected.
        :param path_tracker: Dictionary tracking the path taken.
        :param x, y: Current position coordinates.
        :param nx, ny: Detected loop starting position coordinates.
        :return: List of tuples representing the loop path.
        """
        loop = [(nx, ny)]
        while (x, y) != (nx, ny):
            loop.append((x, y))
            x, y = path_tracker[(x, y)]
        return loop

    @staticmethod
    def get_steps_to_the_farthest_point(loop):
        """
        Calculate the number of steps to the farthest point in the loop.
        :param loop: List of tuples representing the loop path.
        :return: Integer representing the number of steps.
        """
        return len(loop) // 2

    def num_of_tiles_enclosed_by_loop(self, loop):
        """
        Calculate the area enclosed by the loop.
        :param perimeter_points: List of tuples representing the loop perimeter.
        :return: Integer representing the enclosed area.
        """
        area = 0
        n = len(loop)
        for i in range(n):
            j = (i + 1) % n
            area += loop[i][0] * loop[j][1]
            area -= loop[j][0] * loop[i][1]
        area = abs(area) // 2
        return area - n // 2 + 1


def part_one():
    # Read the maze input from a file
    with open("day_10/input.txt") as f:
        maze_input = f.read()

    # Initialize the Maze and MazeSolver
    maze = Maze(maze_input)
    solver = MazeSolver(maze.maze)

    # Find the starting position and solve the maze
    start = maze.find_animal_start()
    loop = solver.find_loop(start)
    farthest_point = solver.get_steps_to_the_farthest_point(loop)

    # Print the result
    print(f"❗️ Steps to the farthest point: {farthest_point}")


def part_two():
    # Read the maze input from a file
    with open("day_10/input.txt") as f:
        maze_input = f.read()

    # Initialize the Maze and MazeSolver
    maze = Maze(maze_input)
    solver = MazeSolver(maze.maze)

    # Find the starting position and solve the maze
    start = maze.find_animal_start()
    loop = solver.find_loop(start)
    enclosed_tiles = solver.num_of_tiles_enclosed_by_loop(loop)

    # Print the result
    print(f"❗️ Enclosed tiles: {enclosed_tiles}")


def test_simple_maze():
    maze_input = """.....
.S-7.
.|.|.
.L-J.
....."""

    maze = Maze(maze_input)
    solver = MazeSolver(maze.maze)
    start = maze.find_animal_start()
    loop = solver.find_loop(start)
    farthest_point = solver.get_steps_to_the_farthest_point(loop)
    assert farthest_point == 4, f"Expected 4, got {farthest_point}"
    print("✅ Simple maze test passed")


def test_complex_maze():
    maze_input = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
    maze = Maze(maze_input)
    solver = MazeSolver(maze.maze)
    start = maze.find_animal_start()
    loop = solver.find_loop(start)
    farthest_point = solver.get_steps_to_the_farthest_point(loop)
    assert farthest_point == 4, f"Expected 4, got {farthest_point}"
    print("✅ Complex maze test passed")


def test_more_complex_maze():
    maze_input = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
    maze = Maze(maze_input)
    solver = MazeSolver(maze.maze)
    start = maze.find_animal_start()
    loop = solver.find_loop(start)
    farthest_point = solver.get_steps_to_the_farthest_point(loop)
    assert farthest_point == 8, f"Expected 8, got {farthest_point}"
    print("✅ More complex maze test passed")


def test_most_complex_maze():
    maze_input = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
    maze = Maze(maze_input)
    solver = MazeSolver(maze.maze)
    start = maze.find_animal_start()
    loop = solver.find_loop(start)
    farthest_point = solver.get_steps_to_the_farthest_point(loop)
    assert farthest_point == 8, f"Expected 8, got {farthest_point}"
    print("✅ Most complex maze test passed")


def test_enclosed_tiles_in_maze():
    maze_input = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
    maze = Maze(maze_input)
    solver = MazeSolver(maze.maze)
    start = maze.find_animal_start()
    loop = solver.find_loop(start)

    enclosed_tiles = solver.num_of_tiles_enclosed_by_loop(loop)
    assert enclosed_tiles == 4, f"Expected 4, got {enclosed_tiles}"
    print("✅ Enclosed tiles in maze test passed")


def test_enclosed_tiles_in_tighter_maze():
    maze_input = """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""
    maze = Maze(maze_input)
    solver = MazeSolver(maze.maze)
    start = maze.find_animal_start()
    loop = solver.find_loop(start)

    enclosed_tiles = solver.num_of_tiles_enclosed_by_loop(loop)
    assert enclosed_tiles == 4, f"Expected 4, got {enclosed_tiles}"
    print("✅ Enclosed tiles in tighter maze test passed")


def test_enclosed_tiles_in_tightest_maze():
    maze_input = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
    maze = Maze(maze_input)
    solver = MazeSolver(maze.maze)
    start = maze.find_animal_start()
    loop = solver.find_loop(start)

    enclosed_tiles = solver.num_of_tiles_enclosed_by_loop(loop)
    assert enclosed_tiles == 10, f"Expected 10, got {enclosed_tiles}"
    print("✅ Enclosed tiles in tightest maze test passed")


if __name__ == "__main__":
    # --- Part One ---
    test_simple_maze()
    test_complex_maze()
    test_more_complex_maze()
    test_most_complex_maze()

    part_one()

    # --- Part Two ---
    test_enclosed_tiles_in_maze()
    test_enclosed_tiles_in_tighter_maze()
    test_enclosed_tiles_in_tightest_maze()

    part_two()
