from ciphers.caesar import CaesarCipher
from analysis.n_gram_scorer import NGramScorer
from analysis.chi_squared_calculator import Chi_Squared_Calculator


class CaesarSolver:

    def __init__(self):
        self.cipher = CaesarCipher()
        self.chi_squared_calculator = Chi_Squared_Calculator()

        self.bigram_scorer = NGramScorer('data/ngrams/english_bigrams.json', 2)
        self.trigram_scorer = NGramScorer('data/ngrams/english_trigrams.json', 3)
        self.quadgram_scorer = NGramScorer('data/ngrams/english_quadgrams.json', 4)

    def solve(self, cipher_text: str, top_n: int = 3) -> list[tuple[int, float, str]]:
        """Solves the cipher and returns the top N most likely shifts, scores, and texts."""
        decoded_texts = self.generate_all_shifts(cipher_text)
        scored_shifts = []

        for shift, decoded_text in decoded_texts.items():
            score = self.score_text(decoded_text)
            scored_shifts.append((shift, score, decoded_text))

        scored_shifts.sort(key=lambda x: x[1])

        return scored_shifts[:top_n]

    def generate_all_shifts(self, cipher_text: str) -> dict[int, str]:
        """Generates all 26 possible shift numbers from cipher text"""
        decoded_texts = {}

        for i in range(0, 26):
            decoded_texts[i] = self.cipher.decrypt(cipher_text, i)

        return decoded_texts

    def score_text(self, text: str) -> float:
        """Scores the text based on the different methods available to get the most reliable results"""
        chi_score = self.chi_squared_test(text)
        ngram_score = self.ngram_log_test(text)

        combined_score = chi_score - (ngram_score * 0.1)
        return combined_score

    def chi_squared_test(self, text: str) -> float:
        return self.chi_squared_calculator.calculate_score(text)

    def ngram_log_test(self, text: str) -> float:
        bigram_score = self.bigram_scorer.score_text(text)
        trigram_score = self.trigram_scorer.score_text(text)
        quadgram_score = self.quadgram_scorer.score_text(text)

        weighted_score = (bigram_score * 0.1) + (trigram_score * 0.3) + (quadgram_score * 0.6)

        return weighted_score