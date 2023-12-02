# --- Day 1: Trebuchet?! ---
# --- Part two ---

# mapping of spelled-out numbers to their numeric equivalents
WORD_TO_DIGIT_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def get_combined_digits(line):
    # positions stores tuples of (idx, digit) for each spelled-out 
    # number found in the line, this helps in replacing the spelled-out numbers 
    # with their corresponding digits, considering their order and overlaps in the string
    positions = [
        (idx, digit)
        for word, digit in WORD_TO_DIGIT_MAP.items()
        for idx in range(len(line))
        if line.startswith(word, idx)
    ]

    # add existing numerical digits and their positions
    positions.extend((idx, ch) for idx, ch in enumerate(line) if ch.isdigit())

    # handle no digits case
    if not positions:
        return 0

    # sort by position idx
    positions.sort(key=lambda x: x[0])

    # extract first and last digit based on combined order
    first, last = positions[0][1], positions[-1][1]
    return int(first + last)

def sum_calibration_values(lines):
    sum = 0
    for line in lines:
        tmp = get_combined_digits(line.strip())
        # print(f"{line.strip()} -> {tmp}")
        sum += tmp

    return sum

def test_calibration_values():
    test_cases = [
        ("two1nine", 29),
        ("eightwothree", 83),
        ("abcone2threexyz", 13),
        ("xtwone3four", 24),
        ("4nineeightseven2", 42),
        ("zoneight234", 14),
        ("7pqrstsixteen", 76),
        ("no digits here", 0)
    ]

    for line, expected in test_cases:
        assert get_combined_digits(line) == expected, f"Failed on {line}"

    assert sum_calibration_values([line for line, _ in test_cases]) == 281, "Sum test failed"
    print("All tests passed")


def main():
    with open("day_1/input.txt") as f:
        lines = f.readlines()
        print(sum_calibration_values(lines))

if __name__ == "__main__":
    # run the test function
    test_calibration_values()

    # execute the main function
    main()
