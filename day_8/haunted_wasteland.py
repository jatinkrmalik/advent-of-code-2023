# Day 8: Haunted Wasteland

# --- Part One ---
import math

class DesertNavigator:
    START_LOCATION = "AAA"
    DESTINATION = "ZZZ"

    def __init__(self):
        self.navigation_map = {}
        self.navigation_instructions = []

    def add_location(self, location, left_choice, right_choice):
        self.navigation_map[location] = (left_choice, right_choice)

    def load_navigation_data(self, navigation_data):
        instructions, location_data = navigation_data.strip().split("\n\n")
        self.navigation_instructions = [
            0 if direction == "L" else 1 for direction in instructions
        ]

        for data in location_data.split("\n"):
            location, choices = data.split(" = ")
            left, right = choices.strip("()").split(", ")
            self.add_location(location, left, right)

    # for part 1
    def navigate_desert(self):
        current_location, steps, instruction_idx = self.START_LOCATION, 0, 0

        while current_location != self.DESTINATION:
            direction = self.navigation_instructions[
                instruction_idx % len(self.navigation_instructions)
            ]
            current_location = self.navigation_map[current_location][direction]
            steps += 1
            instruction_idx += 1

        return steps

    # for part 2
    def navigate_desert_as_ghosts(self):
        current_nodes, steps, instruction_idx = [], 0, 0

        # init current nodes with all nodes with A as their last letter
        for node in self.navigation_map.keys():
            if node[-1] == "A":
                current_nodes.append(node)

        while not self.have_reached_destination(current_nodes):
            print(f"Current nodes: {current_nodes}\tSteps: {steps}")
            next_nodes = []
            direction = self.navigation_instructions[
                instruction_idx % len(self.navigation_instructions)
            ]
            for node in current_nodes:
                next_nodes.append(self.navigation_map[node][direction])

            current_nodes = next_nodes
            steps += 1
            instruction_idx += 1

        print(f"Current nodes: {current_nodes}\tSteps: {steps}")
        return steps

    # check if all nodes have Z as last letter
    def have_reached_destination(self, current_nodes):
        for node in current_nodes:
            if node[-1] != "Z":
                return False

        return True
    
    # part 2 - optimised
    def navigate_through_desert_as_ghosts_lcm(self):
        current_nodes = [node for node in self.navigation_map if node.endswith('A')]
        first_z_steps = [""] * (len(current_nodes) * 2)
        cycle_lengths = [""] * len(current_nodes)
        steps = 0
        max_steps = 1

        cycles_complete = False
        instruction_length = len(self.navigation_instructions)

        while not cycles_complete:
            direction = self.navigation_instructions[steps % instruction_length]
            steps += 1
            for index, node in enumerate(current_nodes):
                if node.endswith('Z'):
                    if first_z_steps[index] != "" and cycle_lengths[index] == "":
                        cycle_lengths[index] = steps - first_z_steps[index + len(current_nodes)]
                    if first_z_steps[index] == "":
                        first_z_steps[index] = node
                        first_z_steps[index + len(current_nodes)] = steps
                
                current_nodes[index] = self.navigation_map[node][direction]

            # Check if all cycles are complete
            cycles_complete = all(cycle_length != "" for cycle_length in cycle_lengths)

        for cycle_length in cycle_lengths:
            max_steps = math.lcm(cycle_length, max_steps)

        return max_steps


def test_navigate_desert():
    test_cases = [
        (
            "RL\n\nAAA = (BBB, CCC)\nBBB = (DDD, EEE)\nCCC = (ZZZ, GGG)\nDDD = (DDD, DDD)\nEEE = (EEE, EEE)\nGGG = (GGG, GGG)\nZZZ = (ZZZ, ZZZ)",
            2,
        ),
        ("LLR\n\nAAA = (BBB, BBB)\nBBB = (AAA, ZZZ)\nZZZ = (ZZZ, ZZZ)", 6),
    ]

    for navigation_data, expected_steps in test_cases:
        navigator = DesertNavigator()
        navigator.load_navigation_data(navigation_data)
        assert (
            navigator.navigate_desert() == expected_steps
        ), f"Test failed with input: {navigation_data}"

    print("test_navigate_desert passed!")


def test_navigate_desert_as_ghosts():
    navigation_data = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    navigator = DesertNavigator()
    navigator.load_navigation_data(navigation_data)
    # number_of_steps = navigator.navigate_desert_as_ghosts()
    number_of_steps = navigator.navigate_through_desert_as_ghosts_lcm()
    assert number_of_steps == 6, f"Expected 6 steps, got {number_of_steps}"
    print("test_navigate_desert_as_ghosts passed!")


# part 1
def navigate_through_desert():
    with open("day_8/input.txt") as file:
        navigation_data = file.read()

    navigator = DesertNavigator()
    navigator.load_navigation_data(navigation_data)
    steps = navigator.navigate_desert()
    print(f"Steps to reach destination: {steps}")


# part 2
def navigate_through_desert_as_ghosts():
    with open("day_8/input.txt") as file:
        navigation_data = file.read()

    navigator = DesertNavigator()
    navigator.load_navigation_data(navigation_data)
    # steps = navigator.navigate_desert_as_ghosts()
    steps = navigator.navigate_through_desert_as_ghosts_lcm()
    print(f"Steps to reach destination as ghosts: {steps}")


if __name__ == "__main__":
    test_navigate_desert()
    navigate_through_desert()

    test_navigate_desert_as_ghosts()
    navigate_through_desert_as_ghosts()