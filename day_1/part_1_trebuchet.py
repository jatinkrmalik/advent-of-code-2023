# --- Day 1: Trebuchet?! ---
# --- Part one ---

def get_combined_digits(line):
    # extract all digits from the input line
    digits = [ch for ch in line if ch.isdigit()]

    # handle cases with no digits found
    if not digits:
        return 0  # or handle as per specific requirements

    # extract the first and last digits, duplicate if only one digit present
    first, last = digits[0], digits[-1] if len(digits) > 1 else digits[0]

    # return the combined integer value
    return int(first + last)

def sum_calibration_values(lines):
    # sum up combined digits values for each line
    return sum(get_combined_digits(line.strip()) for line in lines)

def main():
    # read lines from the file
    with open("input.txt") as f:
        lines = f.readlines()

    # calculate and display the sum of calibration values
    print(sum_calibration_values(lines))

def test_calibration_values():
    # define test cases with expected outcomes
    test_cases = [
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77),
        ("no digits here", 0),
    ]

    # test get_combined_digits function
    for line, expected in test_cases:
        assert get_combined_digits(line) == expected, f"Failed on {line}"

    # test sum_calibration_values function
    assert sum_calibration_values([line for line, _ in test_cases]) == 142, "Sum test failed"

    # indicate all tests passed
    print("All tests passed")

if __name__ == "__main__":
    # run the test function
    test_calibration_values()

    # execute the main function
    main()
    