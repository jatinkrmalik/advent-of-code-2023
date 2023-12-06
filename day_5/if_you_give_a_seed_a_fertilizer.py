# --- Day 5: If You Give A Seed A Fertilizer ---

class AlmanacProcessor:
    def __init__(self, almanac):
        self.almanac = almanac
        self.seeds, self.mappings = self._parse_input(almanac)

    def find_lowest_location_number(self):
        """Finds the lowest location number based on the almanac's rules."""
        lowest_location = float('inf')
        for i in range(0, len(self.seeds), 2):
            start = int(self.seeds[i])
            length = int(self.seeds[i + 1])
            for seed in range(start, start + length):
                current_number = seed
                for map_data in self.mappings:
                    current_number = self._find_mapped_number(current_number, map_data)
                lowest_location = min(lowest_location, current_number)
        return lowest_location

    # part One assumes seeds to be given as a list of integers
    # def _parse_input(self, input_data):
    #     """Parses the input data into seeds and mappings."""
    #     sections = input_data.strip().split('\n\n')
    #     seeds = list(map(int, sections[0].split(': ')[1].split()))
    #     mappings = [section.split(':\n')[1].split('\n') for section in sections[1:]]
    #     return seeds, mappings

    def _parse_input(self, input_data):
        """Parses the input data into seed ranges and mappings."""
        sections = input_data.strip().split('\n\n')
        seed_ranges = sections[0].split(': ')[1].split()
        mappings = [section.split(':\n')[1].split('\n') for section in sections[1:]]
        return seed_ranges, mappings   
    

    # def _generate_seed_list(self, seed_ranges):
    #     """Generates a list of seeds based on the ranges provided in pairs"""
    #     seeds = []
    #     for i in range(0, len(seed_ranges), 2):
    #         start = int(seed_ranges[i])
    #         length = int(seed_ranges[i + 1])
    #         seeds.extend(range(start, start + length))
    #     return seeds
    
    # def _find_mapped_number(self, number, optimized_map):
    #     """Finds the corresponding mapped number using the optimized map."""
    #     return optimized_map.get(number, number)
    
    def _find_mapped_number(self, number, map_data):
        """Finds the corresponding mapped number based on the mapping rules."""
        for line in map_data:
            if line.strip():
                dest_start, src_start, length = map(int, line.split())
                if src_start <= number < src_start + length:
                    return dest_start + (number - src_start)
        return number

def main():
    with open("day_5/input.txt", "r") as f:
        almanac = f.read()

    processor = AlmanacProcessor(almanac)
    lowest_location = processor.find_lowest_location_number()
    print("The lowest location number is:", lowest_location)


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
    lowest_location = processor.find_lowest_location_number()
    # assert lowest_location == 35, f"Tst failed: Expected 35, got {lowest_location}" # As per part 1 logic for seeds
    assert lowest_location == 46, f"Tst failed: Expected 35, got {lowest_location}" # As per part 2 logic for seeds
    print("All tests passed succesfully!")


if __name__ == "__main__":
    # Uncomment the line below to run the test
    # test_find_lowest_location_number()

    main()
