# Day 19 - Aplenty

class MachinePart:
    ACCEPTED = "A"
    REJECTED = "R"

    VALID_STATES = [ACCEPTED, REJECTED]

    def __init__(self, x: int, m: int, a: int, s: int):
        self.ratings = {"x": x, "m": m, "a": a, "s": s}
        self.state = None

    def set_state(self, state: str) -> None:
        if state in [self.ACCEPTED, self.REJECTED]:
            self.state = state
        else:
            raise ValueError(f"Invalid state: {state}")

    def is_unprocessed(self) -> bool:
        return self.state is None

    def __str__(self) -> str:
        ratings_str = ",".join(
            [f"{key}={value}" for key, value in self.ratings.items()]
        )
        return ratings_str


def evaluate_condition(part, condition):
    if "<" in condition:
        variable, value = condition.split("<")
        return part.ratings[variable] < int(value)
    elif ">" in condition:
        variable, value = condition.split(">")
        return part.ratings[variable] > int(value)
    else:
        raise ValueError(f"Invalid condition: {condition}")


def process(workflows: dict, parts_list: list) -> list:
    INITIAL_WORKFLOW_ID = "in"
    CONDITION_SEPARATOR = ":"

    for i, part in enumerate(parts_list):
        # print(f"{i+1}/{len(parts_list)}\n Processing part {part}\n\n")
        worflow_id = INITIAL_WORKFLOW_ID
        while part.is_unprocessed():
            for rule in workflows[worflow_id]:
                if CONDITION_SEPARATOR in rule:
                    condition, worflow_id = rule.split(CONDITION_SEPARATOR)
                    if evaluate_condition(part, condition):
                        if worflow_id in MachinePart.VALID_STATES:
                            part.set_state(worflow_id)
                        break # Break out of for loop and move to new workflow
                elif rule in MachinePart.VALID_STATES:
                    part.set_state(rule)
                else:
                    worflow_id = rule
    return parts_list


def sum_of_rating_of_accepted_parts(parts_list: list) -> int:
    sum = 0
    for part in parts_list:
        if part.state == MachinePart.ACCEPTED:
            sum += (
                part.ratings["x"]
                + part.ratings["m"]
                + part.ratings["a"]
                + part.ratings["s"]
            )
    return sum


def parse_input(input_str: str) -> tuple:
    workflow_str, parts_str = input_str.split("\n\n")
    workflows = {}
    for workflow in workflow_str.split("\n"):
        workflow_name, workflow_rules = workflow.split("{")  # Split on first '{'
        workflow_rules = workflow_rules[:-1]  # Remove trailing '}'
        workflows[workflow_name] = workflow_rules.split(",")

    parts_list = []
    for part in parts_str.split("\n"):
        x, m, a, s = part[1:-1].split(",")
        x = int(x.split("=")[1])
        m = int(m.split("=")[1])
        a = int(a.split("=")[1])
        s = int(s.split("=")[1])
        parts_list.append(MachinePart(x, m, a, s))

    return workflows, parts_list

def part_one():
    with open("day_19/input.txt") as f:
        input_str = f.read()
    workflows, parts_list = parse_input(input_str)
    parts_list = process(workflows, parts_list)
    sum = sum_of_rating_of_accepted_parts(parts_list)
    print(f"❗️ Sum of ratings of accepted parts: {sum}")

def test_sum_of_rating_of_accepted_parts():
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

    workflows, parts_list = parse_input(input_str)
    parts_list = process(workflows, parts_list)
    sum = sum_of_rating_of_accepted_parts(parts_list)
    assert sum == 19114, f"Expected 19114, got {sum}"
    print("✅ sum_of_rating_of_accepted_parts() tests passed")


if __name__ == "__main__":
    test_sum_of_rating_of_accepted_parts()

    part_one()