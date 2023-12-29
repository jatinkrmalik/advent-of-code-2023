# Day 20 - Pulse Propagation

from enum import Enum
from collections import deque
from math import gcd
from functools import reduce

# Constants

# dict to hold the count of inputs for each module
INPUT_TRACKER = {}
# global queue to hold pulses
PULSE_QUEUE = deque()
# to hold the count of low and high pulses
LOW_PULSE_COUNT, HIGH_PULSE_COUNT = 0, 0

# Enums

class State(Enum):
    ON = 1
    OFF = 0


class Pulse(Enum):
    HIGH = 1
    LOW = 0


class ModuleType(Enum):
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    BROADCASTER = "broadcaster"

# Classes

class Module:
    def __init__(self, name):
        self.name = name
        self.destinations = []

    def add_destination(self, module):
        self.destinations.append(module)

    def send_pulse(self, pulse):
        for dest_module in self.destinations:
            PULSE_QUEUE.append((pulse, dest_module.name, self.name))
            update_pulse_count(pulse)

    def receive_pulse(self, pulse, input_name):
        raise NotImplementedError("Subclass must implement receive_pulse method")


class FlipFlopModule(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = State.OFF

    def __repr__(self) -> str:
        return f"Module({self.name} - {self.state})"

    def receive_pulse(self, pulse, src_module):
        if pulse == Pulse.LOW:
            self.state = State.ON if self.state == State.OFF else State.OFF
            self.send_pulse(Pulse.HIGH if self.state == State.ON else Pulse.LOW)


class ConjunctionModule(Module):
    def __init__(self, name, inputs):
        super().__init__(name)
        self.inputs = inputs  # List of input module names
        self.input_states = {input_name: Pulse.LOW for input_name in inputs}

    def __repr__(self) -> str:
        return f"Module({self.name} - {self.input_states})"

    def receive_pulse(self, pulse, src_module):
        self.input_states[src_module] = pulse

        if all(state == Pulse.HIGH for state in self.input_states.values()):
            self.send_pulse(Pulse.LOW)
        else:
            self.send_pulse(Pulse.HIGH)


class BroadcasterModule(Module):
    def receive_pulse(self, pulse, src_module):
        self.send_pulse(pulse)


class UntypedModule(Module):
    def __init__(self, name):
        super().__init__(name)
        self.received_pulses = {Pulse.LOW: 0, Pulse.HIGH: 0}

    def __repr__(self) -> str:
        return f"Module({self.name} - {self.received_pulses})"

    def receive_pulse(self, pulse, src_module):
        self.received_pulses[pulse] += 1


class ModuleFactory:
    @staticmethod
    def create_module(module_identifier):
        if module_identifier.startswith(ModuleType.FLIP_FLOP.value):
            return FlipFlopModule(module_identifier[1:])
        elif module_identifier.startswith(ModuleType.CONJUNCTION.value):
            # Determine the number of inputs for the conjunction module
            name = module_identifier[1:]
            module_inputs = INPUT_TRACKER[name]
            return ConjunctionModule(name, module_inputs)
        elif module_identifier == ModuleType.BROADCASTER.value:
            return BroadcasterModule(module_identifier)
        else:
            return UntypedModule(module_identifier)


class Simulation:
    def __init__(self, modules):
        self.modules = modules

    def run_simulation(self, button_presses):
        for _ in range(button_presses):
            # Simulate button press - send a low pulse to broadcaster
            update_pulse_count(Pulse.LOW)
            self.modules["broadcaster"].receive_pulse(Pulse.LOW, "button")

            # Process pulses in the queue
            while PULSE_QUEUE:
                pulse, dest_module, src_module = PULSE_QUEUE.popleft()
                self.modules[dest_module].receive_pulse(pulse, src_module)

    def run_simulation_until_rx(self):
        button_presses = 0

         # rx_source is the only input for rx i.e. &dn
        rx_source = list(INPUT_TRACKER['rx'])[0]

        # dict to hold the index of the rx caller that received a Pulse.HIGH for the first time
        rx_callers_high_pulse_idx = {caller: 0 for caller in INPUT_TRACKER[rx_source]}

        # break when all the rx callers have received a high pulse for the first time
        while not all(idx > 0 for idx in rx_callers_high_pulse_idx.values()):
            button_presses += 1
            self.modules['broadcaster'].receive_pulse(Pulse.LOW, "button")
            update_pulse_count(Pulse.LOW)

            while PULSE_QUEUE:
                pulse, dest_module, src_module = PULSE_QUEUE.popleft()
                self.modules[dest_module].receive_pulse(pulse, src_module)

                # update the index of the rx caller that received a high pulse for the first time
                if src_module in rx_callers_high_pulse_idx.keys() and  pulse == Pulse.HIGH:
                    rx_callers_high_pulse_idx[src_module] = button_presses

        # lcm formula
        lcm = lambda x, y: x * y // gcd(x, y)
    
        # find LCM for all the values in rx_callers_high_pulse_idx
        return reduce(lcm, list(rx_callers_high_pulse_idx.values()))
    


# Util functions

def update_pulse_count(pulse):
    global LOW_PULSE_COUNT, HIGH_PULSE_COUNT
    if pulse == Pulse.LOW:
        LOW_PULSE_COUNT += 1
    elif pulse == Pulse.HIGH:
        HIGH_PULSE_COUNT += 1


def process_input_count(config_lines):
    global INPUT_TRACKER
    for line in config_lines:
        parts = line.split("->")
        source = parts[0].strip()
        if len(parts) > 1:
            destinations = [dest.strip() for dest in parts[1].split(",")]

            for dest in destinations:
                # Remove any prefix from the destination name
                dest = dest.lstrip("%&")
                source = source.lstrip("%&")
                if dest not in INPUT_TRACKER:
                    INPUT_TRACKER[dest] = set()
                INPUT_TRACKER[dest].add(source)


def setup_modules(config_lines):
    modules = {}
    connections = {}

    for line in config_lines:
        parts = line.split("->")
        source_name = parts[0].strip()
        dest_names = parts[1].split(",") if len(parts) > 1 else []
        clean_source_name = source_name.lstrip("%& ")

        if clean_source_name not in modules:
            modules[clean_source_name] = ModuleFactory.create_module(source_name)

        for dest_name in dest_names:
            if clean_source_name not in connections:
                connections[clean_source_name] = []
            connections[clean_source_name].append(dest_name)

    # Set up connections
    for source_name, dest_names in connections.items():
        for dest_name in dest_names:
            dest_name = dest_name.strip()
            if dest_name not in modules:
                # Create module if it doesn't exist for destination
                modules[dest_name] = ModuleFactory.create_module(dest_name)
            modules[source_name].add_destination(modules[dest_name])

    return modules

# Tests

def test_count_pulses_in_the_circuit_a():
    input_str = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
    process_input_count(input_str.splitlines())
    modules = setup_modules(input_str.splitlines())
    simulation = Simulation(modules)
    button_presses = 1000
    simulation.run_simulation(button_presses)
    num_pulses = LOW_PULSE_COUNT * HIGH_PULSE_COUNT
    assert num_pulses == 32000000, f"Expected 32000000, got {num_pulses}"
    print("✅ test_count_pulses_in_the_circuit_a() passed")


def test_count_pulses_in_the_circuit_b():
    input_str = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
    process_input_count(input_str.splitlines())
    modules = setup_modules(input_str.splitlines())
    simulation = Simulation(modules)
    button_presses = 1000
    simulation.run_simulation(button_presses)
    num_pulses = LOW_PULSE_COUNT * HIGH_PULSE_COUNT
    assert num_pulses == 11687500, f"Expected 11687500, got {num_pulses}"
    print("✅ test_count_pulses_in_the_circuit_b() passed")

# Main

def part_one():
    with open("day_20/input.txt") as f:
        config_lines = f.readlines()
    process_input_count(config_lines)
    modules = setup_modules(config_lines)
    simulation = Simulation(modules)
    button_presses = 1000
    simulation.run_simulation(button_presses)
    num_pulses = LOW_PULSE_COUNT * HIGH_PULSE_COUNT
    print(
        f"❗️ Product of total number of low pulses sent by the \
total number of high pulses sent: {num_pulses}"
    )

def part_two():
    with open("day_20/input.txt") as f:
        config_lines = f.readlines()
    process_input_count(config_lines)
    modules = setup_modules(config_lines)
    simulation = Simulation(modules)
    button_presses = simulation.run_simulation_until_rx()
    print(f"❗️❗️ Number of button presses required to activate the Rx: {button_presses}")


if __name__ == "__main__":
    # test_count_pulses_in_the_circuit_a()
    # test_count_pulses_in_the_circuit_b()
    # part_one()
    part_two()