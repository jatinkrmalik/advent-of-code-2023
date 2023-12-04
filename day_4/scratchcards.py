# --- Day 4: Scratchcards ---

class ScratchCardProcessor:
    """Processes scratch cards to calculate total points and total scratchcards."""
    
    def __init__(self, scratchcards: str):
        """Initializes the processor with a string of scratchcards."""
        self.scratchcards = scratchcards
        self.repository = {self._get_card_id(scratchcard): 1 for scratchcard in self._get_lines()}

    def calculate_total_points(self) -> int:
        """Calculates the total points from all scratchcards."""
        return sum(self._calculate_points(scratchcard) for scratchcard in self._get_lines())
    
    def calculate_total_scratchcards(self) -> int:
        """Calculates the total number of scratchcards."""
        for scratchcard in self._get_lines():
            card_id = self._get_card_id(scratchcard)
            match_count = self._get_match_count(scratchcard)
            for i in range(1, match_count + 1):
                self.repository[card_id + i] += self.repository[card_id]
        
        return sum(self.repository.values())

    def _get_lines(self):
        """Splits the scratchcards string into individual lines."""
        return self.scratchcards.splitlines()

    def _get_card_id(self, scratchcard: str) -> int:
        """Extracts the card ID from a scratchcard string."""
        return int(scratchcard.split(":")[0].split()[1])

    def _get_match_count(self, scratchcard: str) -> int:
        """Calculates the match count for a scratchcard."""
        _, numbers = scratchcard.split(": ")
        winning_numbers, your_numbers = (set(map(int, ns.split())) for ns in numbers.split(" | "))
        return len(your_numbers & winning_numbers)

    def _calculate_points(self, scratchcard: str) -> int:
        """Calculates points for a single scratchcard."""
        match_count = self._get_match_count(scratchcard)
        return 0 if match_count == 0 else 2 ** (match_count - 1)

    @staticmethod
    def test_calculate_total_points():
        scratchcards = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
        processor = ScratchCardProcessor(scratchcards)
        total_points = processor.calculate_total_points()
        assert total_points == 13, f"Expected 13, got {total_points}"
        print("test_calculate_total_points passed!")

    @staticmethod
    def test_calculate_total_scratchcards():
        scratchcards = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
        processor = ScratchCardProcessor(scratchcards)
        total_scratchcards = processor.calculate_total_scratchcards()
        assert total_scratchcards == 30, f"Expected 30, got {total_scratchcards}"
        print("test_calculate_total_scratchcards passed!")

def part_1():
    with open("day_4/input.txt") as f:
        scratchcards = f.read()

    processor = ScratchCardProcessor(scratchcards)
    print(f"Total points: {processor.calculate_total_points()}")

def part_2():
    with open("day_4/input.txt") as f:
        scratchcards = f.read()

    processor = ScratchCardProcessor(scratchcards)
    print(f"Total scratchcards: {processor.calculate_total_scratchcards()}")

if __name__ == "__main__":
    ScratchCardProcessor.test_calculate_total_points()
    part_1()

    ScratchCardProcessor.test_calculate_total_scratchcards()
    part_2()

