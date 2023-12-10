# Day 7: Camel Cards

## Part One

from collections import Counter

class CamelCardsGame:
    HAND_STRENGTH_ORDER = [
        'Five of a kind', 'Four of a kind', 'Full house',
        'Three of a kind', 'Two pair', 'One pair', 'High card'
    ]
    CARD_ORDER = 'AKQJT98765432'

    def __init__(self, hands_input_str):
        self.hands = self.parse_input(hands_input_str)

    def parse_input(self, input_str):
        lines = input_str.strip().split('\n')
        return [(line.split()[0], int(line.split()[1])) for line in lines]

    def classify_hand(self, hand):
        counts = Counter(hand).most_common()
        hand_type = ""
        card_strengths = []

        for card in hand:
            card_strengths.append(self.CARD_ORDER.index(card))

        if counts[0][1] == 5:
            hand_type = 'Five of a kind'
        elif counts[0][1] == 4:
            hand_type = 'Four of a kind'
        elif counts[0][1] == 3 and counts[1][1] == 2:
            hand_type = 'Full house'
        elif counts[0][1] == 3:
            hand_type = 'Three of a kind'
        elif counts[0][1] == 2 and counts[1][1] == 2:
            hand_type = 'Two pair'
        elif counts[0][1] == 2:
            hand_type = 'One pair'
        else:
            hand_type = 'High card'

        return (hand_type, card_strengths)

    def sort_hands(self):
        sorted_hands = []
        for index, (hand, _) in enumerate(self.hands):
            hand_type, card_strengths = self.classify_hand(hand)
            sorted_hands.append((hand_type, card_strengths, index, hand))

        # sort by hand type, then by card strengths
        sorted_hands.sort(key=lambda x: (self.HAND_STRENGTH_ORDER.index(x[0]), x[1]))

        return sorted_hands

    def calculate_winnings(self):
        sorted_hands = self.sort_hands()
        total_winnings = 0
        num_hands = len(sorted_hands)
        for rank, (_, _, index, _) in enumerate(sorted_hands, start=1):
            bid = self.hands[index][1]
            total_winnings += (num_hands - rank + 1) * bid  # Adjust rank for winnings calculation
        return total_winnings


def part_1():
    with open('day_7/input.txt', 'r') as f:
        hands_input = f.read()
    game = CamelCardsGame(hands_input)
    total_winnings = game.calculate_winnings()
    print(f"Total winnings: {total_winnings}")

def test_calculate_winnings():
    # puzzle input contains game hands and their bids
    hands_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

    # Create an instance of CamelCardsGame and calculate total winnings
    game = CamelCardsGame(hands_input)
    total_winnings = game.calculate_winnings()
    assert total_winnings == 6440, f"Expected 6440, got {total_winnings}"
    print("test_calculate_total_winnings passed successfully!")


if __name__ == "__main__":
    test_calculate_winnings()
    part_1()
