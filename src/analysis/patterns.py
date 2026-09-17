from collections import Counter

class PatternAnalyzer:

    def __init__(self, text):
        self.text = text.upper()

    def extract_ngrams(self, text, n) -> list:
        """
        Extracts n-grams from the given text.

        Args:
            text (str): The input text from which to extract n-grams.
            n (int): The size of the n-grams to extract.

        Returns:
            list: A list of n-grams extracted from the text.
        """
        ngrams = []
        for i in range(len(text) - n + 1):
            ngram = text[i: i + n]
            ngrams.append(ngram)
        return ngrams

    def get_ngram_positions(self, text, n) -> dict:
        """
        Finds all n-grams and maps them to their starting indices in the text.

        Args:
            text (str): The input text.
            n (int): The size of the n-grams.

        Returns:
            dict: A dictionary mapping each n-gram to a list of its occurrence indices.
        """
        positions = {}

        for i in range(len(text) - n + 1):
            ngram = text[i: i + n]

            if ngram not in positions:
                positions[ngram] = []

            # Append the current starting index
            positions[ngram].append(i)

        return positions

    def get_ngram_distances(self, positions) -> dict:
        """
        Calculates the distances between consecutive occurrences of repeating n-grams.

        Args:
            positions (dict): A dictionary mapping n-grams to lists of indices.

        Returns:
            dict: A dictionary mapping each repeating n-gram to a list of its interval distances.
        """
        distances = {}

        for ngram, indices in positions.items():
            # Only process n-grams that appear more than once
            if len(indices) > 1:
                ngram_distances = []
                for i in range(len(indices) - 1):
                    # Calculate distance between consecutive indices
                    dist = indices[i + 1] - indices[i]
                    ngram_distances.append(dist)

                distances[ngram] = ngram_distances

        return distances

    def get_factors(self, n) -> list:
        """Returns all factors of a number (excluding 1)"""
        factors = []

        for i in range(2, n + 1):
            if n % i == 0:
                factors.append(i)

        return factors

    def estimate_vigenere_key_length(self, text, n=3, max_key_length=20):
        """Estimate the vigenere key length using Kasiski examination"""
        positions = self.get_ngram_positions(text, n)
        distances = self.get_ngram_distances(positions)

        factor_counts = Counter()

        for n_gram, distance_list in distances.items():
            for distance in distance_list:
                for factor in self.get_factors(distance):
                    if 2 <= factor <= max_key_length:
                        factor_counts[factor] += 1

        return factor_counts.most_common()