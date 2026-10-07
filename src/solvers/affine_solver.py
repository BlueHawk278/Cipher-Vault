from ciphers.affine import AffineCipher
from analysis.n_gram_scorer import NGramScorer
from analysis.ic_calculator import IC_Calculator
from analysis.chi_squared_calculator import Chi_Squared_Calculator
import math

class AffineSolver:

    def __init__(self):
        self.cipher = AffineCipher()
        self.chi_squared_calculator = Chi_Squared_Calculator()
        self.ic_calculator = IC_Calculator()

        self.bigram_scorer = NGramScorer('../../data/ngrams/english_bigrams.json', 2)
        self.trigram_scorer = NGramScorer('../../data/ngrams/english_trigrams.json', 3)
        self.quadgram_scorer = NGramScorer('../../data/ngrams/english_quadgrams.json', 4)

    def solve(self, cipher_text: str, top_n: int = 3) -> list[tuple[int, int, float, str]]:
        """Solves the Affine cipher by testing all valid key pairs and returning the top N results."""
        key_pairs = self.generate_all_key_pairs()
        scored_results = []

        for a, b in key_pairs:
            # Temporarily remove try/except to see the actual error
            decoded_text = self.cipher.decrypt(cipher_text, a, b)
            score = self.score_text(decoded_text)
            scored_results.append((a, b, score, decoded_text))

        scored_results.sort(key=lambda x: x[2])
        return scored_results[:top_n]

    def generate_all_key_pairs(self) -> list[tuple[int, int]]:
        """Generates all 312 valid (a, b) key pairs where a is coprime to 26 and b is 0-25."""
        valid_a = [a for a in range(1, 26) if math.gcd(a, 26) == 1]
        key_pairs = []

        for a in valid_a:
            for b in range(26):
                key_pairs.append((a, b))

        return key_pairs

    def score_text(self, text: str) -> float:
        """Scores the text combining chi-squared, n-grams, and Index of Coincidence."""
        chi_score = self.chi_squared_test(text)
        ngram_score = self.ngram_log_test(text)
        ic_score = self.ic_test(text)

        # Target IC for English text
        target_ic = 0.067

        # Calculate how far the text's IC is from normal English.
        ic_penalty = abs(ic_score - target_ic)

        # Combine scores:
        # - Lower chi_score is better
        # - Higher ngram_score is better
        # - Higher ic_penalty is worse
        combined_score = chi_score - (ngram_score * 0.1) + (ic_penalty * 100)

        return combined_score

    def chi_squared_test(self, text: str) -> float:
        return self.chi_squared_calculator.calculate_score(text)

    def ngram_log_test(self, text: str) -> float:
        bigram_score = self.bigram_scorer.score_text(text)
        trigram_score = self.trigram_scorer.score_text(text)
        quadgram_score = self.quadgram_scorer.score_text(text)

        weighted_score = (bigram_score * 0.1) + (trigram_score * 0.3) + (quadgram_score * 0.6)
        return weighted_score

    def ic_test(self, text: str) -> float:
        return self.ic_calculator.calculate_ic(text)