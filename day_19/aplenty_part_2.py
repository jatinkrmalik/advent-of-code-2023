# Day 19 - Aplenty
# Part Two

class MachinePartRanges:
    ACCEPTED = "A"
    REJECTED = "R"

    def __init__(self):
        self.rating_ranges = {
            "x": (1, 4000),
            "m": (1, 4000),
            "a": (1, 4000),
            "s": (1, 4000),
        }
        self.state = None

    def __repr__(self) -> str:
        return str(self.rating_ranges)

    def copy(self):
        # deep copy
        new_mpr = MachinePartRanges()
        new_mpr.rating_ranges = self.rating_ranges.copy()
        return new_mpr


def evaluate_condition(ranges: MachinePartRanges, condition: str) -> (MachinePartRanges, MachinePartRanges):
    true_range, false_range = ranges.copy(), ranges.copy()

    variable, value = condition.split("<" if "<" in condition else ">")

    if "<" in condition:
        true_range.rating_ranges[variable] = (true_range.rating_ranges[variable][0], int(value) - 1)
        false_range.rating_ranges[variable] = (int(value), false_range.rating_ranges[variable][1])
    elif ">" in condition:
        true_range.rating_ranges[variable] = (int(value) + 1, true_range.rating_ranges[variable][1])
        false_range.rating_ranges[variable] = (false_range.rating_ranges[variable][0], int(value))

    return true_range, false_range


def num_of_combinations_possible(workflows) -> int:
    INITIAL_WORKFLOW_ID = "in"
    accepted_ranges_list = []

    stack = [(MachinePartRanges(), INITIAL_WORKFLOW_ID)]

    while stack:
        ranges, workflow_id = stack.pop()

        if workflow_id == MachinePartRanges.ACCEPTED: 
            accepted_ranges_list.append(ranges)
            continue

        if workflow_id == MachinePartRanges.REJECTED:
            continue

        for rule in workflows[workflow_id]:
            if rule == MachinePartRanges.ACCEPTED:
                accepted_ranges_list.append(ranges)
                break

            if rule == MachinePartRanges.REJECTED:
                break

            if ":" not in rule:
                workflow_id = rule
                stack.append((ranges, workflow_id))
                continue
            
            # rule must be a condition
            condition, new_worflow_id = rule.split(":")
            true_range, false_range = evaluate_condition(ranges, condition) 
            stack.append((true_range, new_worflow_id)) # Add true range to stack to explore new_workflow_id
            ranges = false_range # Update ranges for next iteration in rules loop

    # now we have a list of accepted ranges, we can calculate the number of combinations possible
    num_of_combinations = 0
    for ranges in accepted_ranges_list:
        num_of_combinations += (
            (ranges.rating_ranges["x"][1] - ranges.rating_ranges["x"][0] + 1)
            * (ranges.rating_ranges["m"][1] - ranges.rating_ranges["m"][0] + 1)
            * (ranges.rating_ranges["a"][1] - ranges.rating_ranges["a"][0] + 1)
            * (ranges.rating_ranges["s"][1] - ranges.rating_ranges["s"][0] + 1)
        )

    return num_of_combinations


def parse_input(input_str: str) -> tuple:
    workflow_str, _ = input_str.split("\n\n")
    workflows = {}
    for workflow in workflow_str.split("\n"):
        workflow_name, workflow_rules = workflow.split("{")  # Split on first '{'
        workflow_rules = workflow_rules[:-1]  # Remove trailing '}'
        workflows[workflow_name] = workflow_rules.split(",")

    return workflows

def part_two():
    with open("day_19/input.txt") as f:
        input_str = f.read()
    workflows = parse_input(input_str)
    num = num_of_combinations_possible(workflows)
    print(f"❗️❗️ Number of combinations possible: {num}")

def test_num_of_combinations_possible():
    input_str = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

    workflows = parse_input(input_str)
    num = num_of_combinations_possible(workflows)
    assert num == 167409079868000, f"Expected 167409079868000, got {num}"
    print("✅ sum_of_rating_of_accepted_parts() tests passed")


if __name__ == "__main__":
    test_num_of_combinations_possible()
    part_two()
