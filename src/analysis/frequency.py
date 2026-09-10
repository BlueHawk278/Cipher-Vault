import utils.utils as utils

class Frequency:
    cipher_text = None

    def __init__(self, text: str) -> None:
        self.cipher_text = text

    def format_text(self) -> str:
        """A method to format the cipher text to ensure all text is in uppercase and there are no spaces or punctuation marks."""
        cleaned_text = ""
        for char in self.cipher_text:
            if char in utils.LOWER:
                cleaned_text += char.upper()
            elif char in utils.UPPER:
                cleaned_text += char
        self.cipher_text = cleaned_text

    def get_count(self) -> dict:
        """A method to return the amount of appearances of each letter in the cipher text, including 0 for missing letters."""
        self.format_text()

        # Pre-populate the dictionary with 0 for all uppercase letters
        count = {letter: 0 for letter in utils.UPPER}

        # Count the characters present in the cleaned cipher text
        for char in self.cipher_text:
            if char in count:
                count[char] += 1

        return count

    def get_freq(self) -> dict:
        """A method to return the decimal frequency of each letter relative to the total character count."""
        counts = self.get_count()
        total_chars = len(self.cipher_text)

        # Prevent divide by zero error if given empty input
        if total_chars == 0:
            return {letter: 0.0 for letter in utils.UPPER}

        # Calculate the decimal percentage (e.g., 0.125 for 12.5%)
        frequencies = {letter: count / total_chars for letter, count in counts.items()}
        return frequencies

    def display_count_and_frequency(self) -> None:
        """A method to display a formatted report of the count and decimal frequency of each letter."""
        counts = self.get_count()
        frequencies = self.get_freq()

        print(f"{'Letter':<8} | {'Count':<6} | {'Frequency':<10}")
        print("-" * 30)

        for letter in utils.UPPER:
            count = counts[letter]
            freq = frequencies[letter]
            # :.4f formats the decimal to 4 decimal places
            print(f"{letter:<8} | {count:<6} | {freq:<10.4f}")
