from utils import utils
from analysis.frequency import Frequency

class Chi_Squared_Calculator:

    def calculate_score(self, text: str) -> float:
        frequency = Frequency(text)
        frequency.format_text()

        text_frequency = frequency.get_freq()
        expected_frequency = utils.get_english_letter_frequency_dict()
        total_letters = frequency.get_total_letter_count()

        chi_squared_sum = 0.0

        for char in expected_frequency:
            observed = text_frequency.get(char, 0.0)
            expected = expected_frequency[char]

            # Check for division by zero before doing the math
            if expected > 0:
                chi_squared_sum += ((observed - expected) ** 2) / expected

        chi_squared_score = chi_squared_sum * total_letters

        return chi_squared_score