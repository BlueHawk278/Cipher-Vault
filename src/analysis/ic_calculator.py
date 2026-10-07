from utils import utils
from analysis.frequency import Frequency

class IC_Calculator:

    def calculate_ic(self, text: str) -> float:
        frequency = Frequency(text)
        count = frequency.get_count()
        count = utils.remove_zero_dict(count)

        numerator = self.get_numerator(count)
        denominator = self.get_denominator(count)

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def get_numerator(self, d: dict) -> int:
        if d is None:
            return 0

        numerator = 0
        for key, value in d.items():
            numerator += (value * (value - 1))

        return numerator

    def get_denominator(self, d: dict) -> int:
        if d is None:
            return 0

        # Calculate N (total number of letters) by summing all frequency values
        total_letters = sum(d.values())

        # Denominator for IC is N * (N - 1)
        return total_letters * (total_letters - 1)