# --- Day 5: If You Give A Seed A Fertilizer ---

import multiprocessing

class AlmanacProcessor:
    def __init__(self, almanac):
        self.almanac = almanac
        # self.seeds, self.mappings = self._parse_input(almanac) # part one
        self.seed_ranges, self.mappings = self._parse_input(almanac)

    def _process_sub_range(self, start, end):
        """Process a sub-range of seeds and find the lowest location number in the sub-range."""
        lowest_location = float('inf')
        for seed in range(start, end):          
            current_number = seed
            for map_data in self.mappings:
                current_number = self._find_mapped_number(current_number, map_data)
            lowest_location = min(lowest_location, current_number)
        print(f"Finished processing seed range: {start} to {end}, lowest location: {lowest_location}")
        return lowest_location

    def _process_seed_range(self, start, length, pool):
        """Process a range of seeds in parallel sub-ranges."""
        sub_range_size = 1000
        results = []
        for sub_start in range(start, start + length, sub_range_size):
            sub_end = min(sub_start + sub_range_size, start + length)
            print(f"Spawning a sub-process process for seed range: {sub_start} to {sub_end}")
            result = pool.apply_async(self._process_sub_range, args=(sub_start, sub_end))
            results.append(result)
        # Retrieve and compare the results from each sub-range
        return min(result.get() for result in results)

    def find_lowest_location_number(self):
        """Finds the lowest location number using parallel processing."""
        with multiprocessing.Pool() as pool:
            range_results = []
            for i in range(0, len(self.seed_ranges), 2):
                start = int(self.seed_ranges[i])
                length = int(self.seed_ranges[i + 1])
                print(f"Spawning a process for seed range: {start} to {start + length}")
                range_result = self._process_seed_range(start, length, pool)
                range_results.append(range_result)
            # Retrieve and compare the results from each range
            lowest_location = min(range_results)
        return lowest_location

    # def find_lowest_location_number(self):
    #     """Finds the lowest location number based on the almanac's rules."""
    #     lowest_location = float('inf')
    #     for i in range(0, len(self.seed_ranges), 2):
    #         start = int(self.seed_ranges[i])
    #         length = int(self.seed_ranges[i + 1])
    #         print(f"Processing seed from {start} to {start + length}")

    #         for seed in range(start, start + length):          
    #             current_number = seed

    #             for map_data in self.mappings:
    #                 current_number = self._find_mapped_number(current_number, map_data)
    #             lowest_location = min(lowest_location, current_number)
    #     return lowest_location


    def _parse_input(self, input_data):
        """Parses the input data into seed ranges and mappings."""
        sections = input_data.strip().split('\n\n')
        seed_ranges = sections[0].split(': ')[1].split()
        mappings = [section.split(':\n')[1].split('\n') for section in sections[1:]]
        return seed_ranges, mappings   
    
    def _find_mapped_number(self, number, map_data):
        """Finds the corresponding mapped number based on the mapping rules."""
        for line in map_data:
            if line.strip():
                dest_start, src_start, length = map(int, line.split())
                if src_start <= number < src_start + length:
                    return dest_start + (number - src_start)
        return number
    
    # part One assumes seeds to be given as a list of integers
    # def _parse_input(self, input_data):
    #     """Parses the input data into seeds and mappings."""
    #     sections = input_data.strip().split('\n\n')
    #     seeds = list(map(int, sections[0].split(': ')[1].split()))
    #     mappings = [section.split(':\n')[1].split('\n') for section in sections[1:]]
    #     return seeds, mappings

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
    test_find_lowest_location_number()

    # main()
