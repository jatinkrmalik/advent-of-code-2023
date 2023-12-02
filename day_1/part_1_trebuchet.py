# --- Day 1: Trebuchet?! ---
# --- Part one ---
def get_combined_digits(line):
    digits = [ch for ch in line if ch.isdigit()]
    first, last = digits[0], digits[-1] if len(digits) > 1 else digits[0]
    return int(first + last)

def sum_calibration_values(lines):
    return sum(get_combined_digits(line.strip()) for line in lines)

def main():
    with open("input.txt") as f:
        lines = f.readlines()
        print(sum_calibration_values(lines))

if __name__ == "__main__":
    # test_calibration_values()
    main()


def test_calibration_values():
    test_cases = [
        ("1abc2", 12),
        ("pqr3stu8vwx", 38),
        ("a1b2c3d4e5f", 15),
        ("treb7uchet", 77),
    ]

    for line, expected in test_cases:
        assert get_combined_digits(line) == expected

    assert sum_calibration_values([line for line, _ in test_cases]) == 142
    print("All tests passed")
