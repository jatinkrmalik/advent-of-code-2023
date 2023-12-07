# --- Day 6: Wait For It ---

class Boat:
    def __init__(self, speed=0):
        self.speed = speed # initial speed: 0 mm/ms

    def charge(self):
        """Increase the speed of the boat by 1 unit."""
        self.speed += 1 # Charge: +1 mm/ms 

    def distance(self, time):
        """Calculate the distance covered by the boat in a given time."""
        return self.speed * time

    def reset(self):
        """Reset the speed of the boat to its initial state."""
        self.speed = 0


class RaceAnalyzer:
    def __init__(self):
        self.boat = Boat()

    # --- For Part One ---
    @staticmethod
    def parse_race_records_part_1(raw_race_records):
        """Parse raw race records into a list of tuples containing time and distance."""
        time_list = [int(t) for t in raw_race_records.splitlines()[0].split(":")[1].strip().split()]
        distance_list = [int(t) for t in raw_race_records.splitlines()[1].split(":")[1].strip().split()]
        return list(zip(time_list, distance_list))
    
    # --- For Part Two ---
    @staticmethod
    def parse_race_records_part_2(raw_race_records):
        """Parse raw race records into a list of tuples containing time and distance."""
        record_time = int(raw_race_records.splitlines()[0].split(":")[1].replace(" ", "").strip())
        record_distance = int(raw_race_records.splitlines()[1].split(":")[1].replace(" ", "").strip())
        return [(record_time, record_distance)]

    def find_number_of_ways_to_win(self, record_time, record_distance):
        """Determine the number of ways the boat can win given the record time and distance."""
        self.boat.reset()
        ways_to_win = 0

        for charging_time in range(1, record_time):
            self.boat.charge()
            boat_distance = self.boat.distance(record_time - charging_time)

            # improve performance by breaking early if the boat can't win
            if ways_to_win > 0 and boat_distance <= record_distance:
                break
            
            if  boat_distance > record_distance:
                ways_to_win += 1

        return ways_to_win

    def product_of_ways_to_win(self, race_records):
        """Calculate the product of ways to win for multiple race records."""
        prod = 1
        for record_time, record_distance in race_records:
            prod *= self.find_number_of_ways_to_win(record_time, record_distance)
        return prod


def part_1():
    analyzer = RaceAnalyzer()
    with open("day_6/input.txt", "r") as f:
        raw_race_records = f.read()

    race_records = analyzer.parse_race_records_part_1(raw_race_records)
    margin_of_error = analyzer.product_of_ways_to_win(race_records)
    print(f"Margin of error: {margin_of_error}")

def part_2():
    analyzer = RaceAnalyzer()
    with open("day_6/input.txt", "r") as f:
        raw_race_records = f.read()

    race_records = analyzer.parse_race_records_part_2(raw_race_records)
    margin_of_error = analyzer.product_of_ways_to_win(race_records)
    print(f"Margin of error: {margin_of_error}")

def test_find_number_of_ways_to_win_part_1():
    raw_race_records = """Time:      7  15   30
Distance:  9  40  200"""

    analyzer = RaceAnalyzer()
    race_records = analyzer.parse_race_records_part_1(raw_race_records)
    margin_of_error = analyzer.product_of_ways_to_win(race_records)
    assert margin_of_error == 288, f"Expected 288, got {margin_of_error}"
    print("All tests passed successfully!")


def test_find_number_of_ways_to_win_part_2():
    raw_race_records = """Time:      7  15   30
Distance:  9  40  200"""

    analyzer = RaceAnalyzer()
    race_records = analyzer.parse_race_records_part_2(raw_race_records)
    margin_of_error = analyzer.product_of_ways_to_win(race_records)
    assert margin_of_error == 71503, f"Expected 288, got {margin_of_error}"
    print("All tests passed successfully!")

if __name__ == "__main__":
    # part 1
    test_find_number_of_ways_to_win_part_1()
    part_1()

    # part 2
    test_find_number_of_ways_to_win_part_2()
    part_2()