class PatternAnalyzer:

    def __init__(self, text):
        self.text = text.Upper()

    def extract_ngrams(self, text, n):
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

    def get_ngram_positions(self, text, n):
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

    def cget_ngram_distances(self, positions):
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