from analysis.scoring import Scorer
from ciphers.trithemius import TrithemiusCipher


class TrithemiusSolver:

    def __init__(self):
        self.cipher = TrithemiusCipher()
        self.scorer = Scorer()

    def solve(self, cipher_text: str, expected_key: int = None) -> list[tuple[int, float, str]]:
        scored_results = []

        for key in range(26):
            decoded_text = self.cipher.decrypt(cipher_text, key)
            score = self.scorer.score_text(decoded_text)
            scored_results.append((key, score, decoded_text))

        scored_results.sort(key=lambda x: x[1])

        return scored_results[:1]