from enum import Enum
from functools import cache


class SpringState(Enum):
    OPERATIONAL = "."
    DAMAGED = "#"
    UNKNOWN = "?"


@cache
def get_valid_spring_record_combinations(spring_state, damaged_spring_record):
    if not damaged_spring_record:
        if SpringState.DAMAGED.value in spring_state:
            return 0
        else:
            return 1

    if not spring_state:
        if not damaged_spring_record:
            return 1
        else:
            return 0

    total_combinations = 0

    # if "." or "?"
    if spring_state[0] in [SpringState.OPERATIONAL.value, SpringState.UNKNOWN.value]:
        total_combinations += get_valid_spring_record_combinations(
            spring_state[1:], damaged_spring_record
        )

    # if "#" or "?"
    if spring_state[0] in [SpringState.DAMAGED.value, SpringState.UNKNOWN.value]:
        if is_valid_condition(spring_state, damaged_spring_record):
            total_combinations += get_valid_spring_record_combinations(
                spring_state[damaged_spring_record[0] + 1 :], damaged_spring_record[1:]
            )

    return total_combinations


def is_valid_condition(spring_state, damaged_spring_record):
    return (
        damaged_spring_record[0] <= len(spring_state)
        and SpringState.OPERATIONAL.value
        not in spring_state[: damaged_spring_record[0]]
        and (
            damaged_spring_record[0] == len(spring_state)
            or spring_state[damaged_spring_record[0]] != SpringState.DAMAGED.value
        )
    )


def sum_spring_record_combinations(spring_condition_records):
    total_combinations = 0
    for spring_record in spring_condition_records.splitlines():
        spring_state, damaged_spring_record = spring_record.split()
        damaged_spring_record = tuple(map(int, damaged_spring_record.split(",")))
        total_combinations += get_valid_spring_record_combinations(
            spring_state, damaged_spring_record
        )

    return total_combinations


def part_one():
    with open("day_12/input.txt") as f:
        spring_condition_records = f.read()
    sum = sum_spring_record_combinations(spring_condition_records)
    print(f"❗️ Total valid combinations: {sum}")


def sum_spring_record_combinations_unfold(spring_condition_records):
    total_combinations = 0
    for spring_record in spring_condition_records.splitlines():
        spring_state, damaged_spring_record = spring_record.split()
        damaged_spring_record = tuple(map(int, damaged_spring_record.split(",")))
        spring_state = "?".join([spring_state] * 5)  # unfolding
        damaged_spring_record = damaged_spring_record * 5  # unfolding
        total_combinations += get_valid_spring_record_combinations(
            spring_state, damaged_spring_record
        )

    return total_combinations


def part_two():
    with open("day_12/input.txt") as f:
        spring_condition_records = f.read()
    sum = sum_spring_record_combinations_unfold(spring_condition_records)
    print(f"❗️ Total valid combinations: {sum}")


def test_sum_spring_record_combinations():
    spring_condition_records = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    sum = sum_spring_record_combinations(spring_condition_records)
    assert sum == 21, f"❌ Expected: 21, Actual: {sum}"
    print("✅ OK - test_sum_spring_record_combinations")


def test_sum_unfolded_spring_record_combinations():
    spring_condition_records = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
    sum = sum_spring_record_combinations_unfold(spring_condition_records)
    assert sum == 525152, f"❌ Expected: 525152, Actual: {sum}"
    print("✅ OK - test_sum_unfolded_spring_record_combinations")


if __name__ == "__main__":
    test_sum_spring_record_combinations()
    part_one()

    test_sum_unfolded_spring_record_combinations()
    part_two()
