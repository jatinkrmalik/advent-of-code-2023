# Day 15: Lens Library

from enum import Enum


class Operation(Enum):
    DASH = "-"
    EQUALS = "="


# Represents a step in the initialization sequence, parsing its components
class Step:
    def __init__(self, step):
        # Check if the step involves removing a lens (indicated by a dash)
        if Operation.DASH.value in step:
            self.label, _ = step.split(Operation.DASH.value)
            self.operation = Operation.DASH
            self.focal_length = None

        # Check if the step involves adding or updating a lens (indicated by an equals sign)
        elif Operation.EQUALS.value in step:
            self.label, focal_length = step.split(Operation.EQUALS.value)
            self.operation = Operation.EQUALS
            self.focal_length = int(focal_length)

        else:
            raise ValueError(f"Invalid step: {step}")


# Represents a lens with a label and focal length
class Lens:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __repr__(self):
        return f"[{self.label} {self.focal_length}]"


# Represents a box that can hold multiple lenses
class Box:
    def __init__(self, id):
        self.id = id
        self.lenses = []

    def find_lens(self, label):
        for lens in self.lenses:
            if lens.label == label:
                return lens
        return None

    def remove_lens(self, label):
        lens = self.find_lens(label)
        if lens:
            self.lenses.remove(lens)

    def add_or_update_lens(self, lens):
        existing_lens = self.find_lens(lens.label)
        if existing_lens:
            existing_lens.focal_length = lens.focal_length
        else:
            self.lenses.append(lens)

    def calc_focusing_power(self):
        return sum(
            (self.id + 1) * (idx + 1) * lens.focal_length
            for idx, lens in enumerate(self.lenses)
        )


# Represents the entire Lava Production Facility with its boxes
class LavaProductionFacility:
    def __init__(self):
        self.boxes = [Box(id) for id in range(256)]

    # H.A.S.H.M.A.P. = Holiday ASCII String Helper Manual Arrangement Procedure
    def holiday_ascii_string_helper_manual_arrangement_procedure(self, sequence_steps):
        for step in sequence_steps:
            step_obj = Step(step)
            box_id = self.holiday_ascii_string_helper(step_obj.label)
            box = self.boxes[box_id]

            if step_obj.operation == Operation.DASH:
                box.remove_lens(step_obj.label)
            elif step_obj.operation == Operation.EQUALS:
                lens = Lens(step_obj.label, step_obj.focal_length)
                box.add_or_update_lens(lens)

    def sum_focusing_power(self):
        return sum(box.calc_focusing_power() for box in self.boxes)

    @staticmethod
    # H.A.S.H. = Holiday ASCII String Helper
    def holiday_ascii_string_helper(step):
        current_value = 0
        for ch in step:
            current_value = (current_value + ord(ch)) * 17 % 256
        return current_value

    def get_sequence_hash(self, sequence):
        return sum(
            self.holiday_ascii_string_helper(step) for step in sequence.split(",")
        )


def part_one():
    with open("day_15/input.txt") as f:
        sequence = f.read().strip()

    facility = LavaProductionFacility()
    sum_hash = facility.get_sequence_hash(sequence)
    print(f"❗️ Part One: {sum_hash}")


def part_two():
    with open("day_15/input.txt") as f:
        sequence = f.read().strip()

    facility = LavaProductionFacility()
    facility.holiday_ascii_string_helper_manual_arrangement_procedure(
        sequence.split(",")
    )
    sum_focusing_power = facility.sum_focusing_power()
    print(
        f"❗️❗️ Focusing power of the resulting lens configuration: {sum_focusing_power}"
    )


def test_hashmap():
    sequence = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    facility = LavaProductionFacility()
    facility.holiday_ascii_string_helper_manual_arrangement_procedure(
        sequence.split(",")
    )
    sum_focusing_power = facility.sum_focusing_power()
    assert sum_focusing_power == 145, f"Expected 145, but got {sum_focusing_power}"
    print("✅ test_hashmap Passed")


def test_get_sequence_hash():
    sequence = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    facility = LavaProductionFacility()
    sum_hash = facility.get_sequence_hash(sequence)
    assert sum_hash == 1320, f"Expected 1320, but got {sum_hash}"
    print("✅ test_process_sequence Passed")


if __name__ == "__main__":
    test_get_sequence_hash()
    part_one()

    test_hashmap()
    part_two()
