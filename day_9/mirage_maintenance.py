# --- Day 9: Mirage Maintenance ---

class OasisAnalyzer:
    def __init__(self, report):
        self.report = report.splitlines()

    def extrapolate_next_value(self, history_line):
        sequence = [int(x) for x in history_line.split(" ")]
        sequences = [sequence]

        while True:
            next_sequence = [sequences[-1][i + 1] - sequences[-1][i] for i in range(len(sequences[-1]) - 1)]
            sequences.append(next_sequence)

            if all(v == 0 for v in next_sequence):
                break

        return sum(row[-1] for row in sequences)

    def extrapolate_previous_value(self, history_line):
        sequence = [int(x) for x in history_line.split(" ")]
        sequences = [sequence]

        while True:
            next_sequence = [sequences[-1][i + 1] - sequences[-1][i] for i in range(len(sequences[-1]) - 1)]
            sequences.append(next_sequence)

            if all(v == 0 for v in next_sequence):
                break

        sequences[-1] = [0] + sequences[-1]
        for i in range(len(sequences) - 2, -1, -1):
            sequences[i].insert(0, sequences[i][0] - sequences[i + 1][0])

        return sequences[0][0]

    def process_report(self, extrapolate_backwards=False):
        if extrapolate_backwards:
            return sum(self.extrapolate_previous_value(row) for row in self.report)
        
        return sum(self.extrapolate_next_value(row) for row in self.report)


def part_one():
    with open("day_9/input.txt", "r") as f:
        report = f.read()

    analyzer = OasisAnalyzer(report)
    sum_of_extrapolated_values = analyzer.process_report()
    print(f"Sum of forward extrapolated values: {sum_of_extrapolated_values}")

def part_two():
    with open("day_9/input.txt", "r") as f:
        report = f.read()

    analyzer = OasisAnalyzer(report)
    sum_of_extrapolated_values = analyzer.process_report(extrapolate_backwards=True)
    print(f"Sum of backward extrapolated values: {sum_of_extrapolated_values}")

def test_process_oasis_report_forward():
    report = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

    analyzer = OasisAnalyzer(report)
    sum_of_extrapolated_values = analyzer.process_report()
    assert sum_of_extrapolated_values == 114, f"Expected 114, got {sum_of_extrapolated_values}"
    print("✅ process_oasis_report_forward passed")

def test_process_oasis_report_backward():
    report = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

    analyzer = OasisAnalyzer(report)
    sum_of_extrapolated_values = analyzer.process_report(extrapolate_backwards=True)
    assert sum_of_extrapolated_values == 2, f"Expected 2, got {sum_of_extrapolated_values}"
    print("✅ process_oasis_report_backward passed")

if __name__ == "__main__":
    test_process_oasis_report_forward()
    part_one()

    test_process_oasis_report_backward()
    part_two()
