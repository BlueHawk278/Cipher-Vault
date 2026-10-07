from ciphers.vigenere import VigenereCipher
from analysis.ic_calculator import IC_Calculator
from analysis.chi_squared_calculator import Chi_Squared_Calculator
from analysis.n_gram_scorer import NGramScorer
from solvers.caesar_solver import CaesarSolver
import utils.utils as utils


class VigenereSolver:

    def __init__(self):
        self.cipher = VigenereCipher()
        self.chi_squared_calculator = Chi_Squared_Calculator()
        self.ic_calculator = IC_Calculator()
        self.caesar_solver = CaesarSolver()

        self.bigram_scorer = NGramScorer('../../data/ngrams/english_bigrams.json', 2)
        self.trigram_scorer = NGramScorer('../../data/ngrams/english_trigrams.json', 3)
        self.quadgram_scorer = NGramScorer('../../data/ngrams/english_quadgrams.json', 4)

    def solve(self, cipher_text: str, max_key_length: int = 12, top_n: int = 3) -> list[tuple[str, str, float]]:
        """
        Automated Vigenere Solver testing key lengths 1 to max_key_length,
        using direct index-based stream slicing to match VigenereCipher.
        """
        results = []

        for k in range(1, max_key_length + 1):
            if k >= len(cipher_text):
                continue

            # 1. Split ciphertext into k streams by exact index position (i % k)
            # This preserves index alignment with VigenereCipher's extendedKey lookup
            streams = ['' for _ in range(k)]
            for i, char in enumerate(cipher_text):
                streams[i % k] += char

            # 2. Solve each stream using your CaesarSolver
            key_chars = []
            for stream in streams:
                # Filter stream for letters to let CaesarSolver do frequency analysis
                alpha_stream = "".join([c for c in stream if c.isalpha()])
                if not alpha_stream:
                    key_chars.append('A')
                    continue

                caesar_results = self.caesar_solver.solve(alpha_stream, top_n=1)
                if caesar_results:
                    best_shift = caesar_results[0][0]
                    key_chars.append(utils.UPPER[best_shift])
                else:
                    key_chars.append('A')

            # 3. Recombine key and decrypt original ciphertext
            estimated_key = "".join(key_chars)
            plaintext = self.cipher.decrypt(cipher_text, estimated_key)

            # 4. Score the combined plaintext
            score = self.score_text(plaintext)
            results.append((estimated_key, plaintext, score))

        # Sort by score in ascending order (lower combined score is better)
        results.sort(key=lambda x: x[2])
        return results[:top_n]

    def score_text(self, text: str) -> float:
        chi_score = self.chi_squared_test(text)
        ngram_score = self.ngram_log_test(text)
        return chi_score - (ngram_score * 0.1)

    def chi_squared_test(self, text: str) -> float:
        return self.chi_squared_calculator.calculate_score(text)

    def ic_test(self, text: str) -> float:
        return self.ic_calculator.calculate_ic(text)

    def ngram_log_test(self, text: str) -> float:
        bigram_score = self.bigram_scorer.score_text(text)
        trigram_score = self.trigram_scorer.score_text(text)
        quadgram_score = self.quadgram_scorer.score_text(text)
        return (bigram_score * 0.1) + (trigram_score * 0.3) + (quadgram_score * 0.6)