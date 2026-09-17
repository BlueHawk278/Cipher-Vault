import utils.utils as utils
from analysis.frequency import Frequency as Frequency

class ic_calculator:
    def calculate_ic(self, text: str) -> float:
        count = Frequency.get_count(text)
        count = utils.remove_zero_dict(count)

        numerator = self.get_numerator(count)
        denominator = self.get_denominator(count)

        return numerator / denominator

    def get_numerator(self, d: dict) -> int:
        numerator = 0

        for key, value in d.items():
            numerator += (value * (value - 1))

        return numerator

    def get_denominator(self, d: dict) -> int:
        num_values = 0

        for key, value in d.items():
            num_values += 1

        return num_values * (num_values - 1)


class chi_squared_calculator:

    def __init__(self, text: str):
        self.text = text

        # This formats the text and gets the relative frequencies for all the letters in the text
        frequency = Frequency(self.text)
        frequency.format_text()

        self.text_frequency = frequency.get_freq()
        self.expected_frequency = utils.get_english_letter_frequency_dict()
        self.total_letters = frequency.get_total_letter_count()

    def calculate_score(self) -> float:
        chi_squared_sum = 0.0

        for char in self.expected_frequency:
            # Use .get() to safely handle letters missing from the text
            observed = self.text_frequency.get(char, 0.0)
            expected = self.expected_frequency[char]

            # Check for division by zero before doing the math
            if expected > 0:
                chi_squared_sum += ((observed - expected) ** 2) / expected

        chi_squared_score = chi_squared_sum * self.total_letters

        return chi_squared_score