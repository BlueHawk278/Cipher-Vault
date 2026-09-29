from ciphers.caesar import CaesarCipher
from analysis.scoring import NGramScorer
from analysis.statistics import chi_squared_calculator

class CaesarSolver:

    def __init__(self):
        self.cipher = CaesarCipher()
        self.chi_squared_calculator = chi_squared_calculator

        self.bigram_scorer = NGramScorer('../../data/ngrams/english_bigrams.json', 2)
        self.trigram_scorer = NGramScorer('../../data/ngrams/english_trigrams.json', 3)
        self.quadgram_scorer = NGramScorer('../../data/ngrams/english_quadgrams.json', 4)

    def solve(self, cipher_text: str, top_n: int = 3) -> list[tuple[int, float, str]]:
        """Solves the cipher and returns the top N most likely shifts, scores, and texts."""
        decoded_texts = self.generate_all_shifts(cipher_text)
        scored_shifts = []

        for shift, decoded_text in decoded_texts.items():
            score = self.score_text(decoded_text)
            scored_shifts.append((shift, score, decoded_text))

        # Sort by score in ascending order (lower score is better)
        scored_shifts.sort(key=lambda x: x[1])

        # Return the top N results
        return scored_shifts[:top_n]

    def generate_all_shifts(self, cipher_text: str) -> dict[int, str]:
        """Generates all 26 possible shift numbers from cipher text"""
        decoded_texts = {}

        for i in range(0, 26):
            decoded_text = self.cipher.decrypt(cipher_text, i)
            decoded_texts[i] = decoded_text

        return decoded_texts

    def score_text(self, text: str) -> float:
        """Scores the text based on the different methods available to get the most reliable results"""
        chi_score = self.chi_squared_test(text)
        ngram_score = self.ngram_log_test(text)

        combined_score = chi_score - (ngram_score * 0.1)
        return combined_score

    def chi_squared_test(self, text: str) -> float:
        calculator = self.chi_squared_calculator(text)
        return calculator.calculate_score()

    def ngram_log_test(self, text: str) -> float:
        bigram_score = self.bigram_scorer.score_text(text)
        trigram_score = self.trigram_scorer.score_text(text)
        quadgram_score = self.quadgram_scorer.score_text(text)

        # Quadgrams are usually the most reliable for English,
        # so they get a higher weight than bigrams or trigrams
        weighted_score = (bigram_score * 0.1) + (trigram_score * 0.3) + (quadgram_score * 0.6)

        return weighted_score
