# --- Day 5: If You Give A Seed A Fertilizer ---

# --- Part Two ---

class AlmanacProcessor:
    def __init__(self, almanac):
        self.seeds = []
        self.maps = []
        self._parse_input(almanac)

    def _parse_input(self, almanac):
        """Parses the input sections into seeds and maps."""
        self.sections = [block.splitlines() for block in almanac.strip().split("\n\n")]
        self.seeds = [int(i) for i in self.sections[0][0].split()[1:]]
        self.maps = [[list(map(int, line.split())) for line in block[1:]] for block in self.sections[1:]]

    def process_maps(self):
        """Processes each map to convert the ranges according to the almanac."""
        # this will store the lower and upper bounds of each range
        values = [(self.seeds[i], self.seeds[i] + self.seeds[i + 1]) for i in range(0, len(self.seeds), 2)] 

        for map in self.maps:
            next_map = []
            for dest_start, src_start, length in map:
                next_range = []
                for val_low, val_high in values:
                    sorted_bounds = sorted([val_low, val_high, src_start, src_start + length])
                    for low, high in zip(sorted_bounds, sorted_bounds[1:]):
                        if val_low <= low < high <= val_high:
                            if src_start <= low < high <= src_start + length:
                                next_map.append((low - src_start + dest_start, high - src_start + dest_start))
                            else:
                                next_range.append((low, high))
                values = next_range
            values += next_map

        return values

    def find_minimum_location(self, values):
        """Finds the minimum location value."""
        return min(low for low, high in values)

def test_find_lowest_location_number():
    almanac = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

    processor = AlmanacProcessor(almanac)
    values = processor.process_maps()
    lowest_location = processor.find_minimum_location(values)
    assert lowest_location == 46, f"Tst failed: Expected 35, got {lowest_location}" # As per part 2 logic for seeds
    print("All tests passed succesfully!")

def main():
    with open("day_5/input.txt", "r") as f:
        almanac = f.read()

    processor = AlmanacProcessor(almanac)
    values = processor.process_maps()
    min_location = processor.find_minimum_location(values)

    print(f"Minimum location number: {min_location}")

if __name__ == "__main__":
    test_find_lowest_location_number()
    main()
