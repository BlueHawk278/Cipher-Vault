from analysis.scoring import Scorer
from ciphers.affine import AffineCipher
import math

class AffineSolver:

    def __init__(self):
        self.cipher = AffineCipher()
        self.scorer = Scorer()

    def solve(self, cipher_text: str, top_n: int = 3) -> list[tuple[int, int, float, str]]:
        """Solves the Affine cipher by testing all valid key pairs and returning the top N results."""
        key_pairs = self.generate_all_key_pairs()
        scored_results = []

        for a, b in key_pairs:
            decoded_text = self.cipher.decrypt(cipher_text, a, b)
            score = self.scorer.score_text(decoded_text)
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
