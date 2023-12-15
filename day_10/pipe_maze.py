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

    def find_cycle(self, start):
        """
        Find the cycle in the maze starting from the given position.
        :param start: Tuple (x, y) as the starting position.
        :return: List of tuples representing the cycle path.
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
                        return self.construct_cycle(path_tracker, x, y, nx, ny)
        raise ValueError("No cycle found")

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

    def construct_cycle(self, path_tracker, x, y, nx, ny):
        """
        Construct the cycle path when a cycle is detected.
        :param path_tracker: Dictionary tracking the path taken.
        :param x, y: Current position coordinates.
        :param nx, ny: Detected cycle starting position coordinates.
        :return: List of tuples representing the cycle path.
        """
        cycle = [(nx, ny)]
        while (x, y) != (nx, ny):
            cycle.append((x, y))
            x, y = path_tracker[(x, y)]
        return cycle

    @staticmethod
    def get_steps_to_the_farthest_point(cycle):
        """
        Calculate the number of steps to the farthest point in the cycle.
        :param cycle: List of tuples representing the cycle path.
        :return: Integer representing the number of steps.
        """
        return len(cycle) // 2


def part_one():
    # Read the maze input from a file
    with open("day_10/input.txt") as f:
        maze_input = f.read()

    # Initialize the Maze and MazeSolver
    maze = Maze(maze_input)
    solver = MazeSolver(maze.maze)

    # Find the starting position and solve the maze
    start = maze.find_animal_start()
    cycle = solver.find_cycle(start)
    farthest_point = solver.get_steps_to_the_farthest_point(cycle)

    # Print the result
    print(f"❗️ Steps to the farthest point: {farthest_point}")


def test_simple_maze():
    maze_input = """.....
.S-7.
.|.|.
.L-J.
....."""

    maze = Maze(maze_input)
    solver = MazeSolver(maze.maze)
    start = maze.find_animal_start()
    cycle = solver.find_cycle(start)
    farthest_point = solver.get_steps_to_the_farthest_point(cycle)
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
    cycle = solver.find_cycle(start)
    farthest_point = solver.get_steps_to_the_farthest_point(cycle)
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
    cycle = solver.find_cycle(start)
    farthest_point = solver.get_steps_to_the_farthest_point(cycle)
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
    cycle = solver.find_cycle(start)
    farthest_point = solver.get_steps_to_the_farthest_point(cycle)
    assert farthest_point == 8, f"Expected 8, got {farthest_point}"
    print("✅ Most complex maze test passed")


if __name__ == "__main__":
    test_simple_maze()
    test_complex_maze()
    test_more_complex_maze()
    test_most_complex_maze()

    part_one()
