from analysis.scoring import Scorer
from ciphers.vigenere import VigenereCipher
from solvers.caesar_solver import CaesarSolver
import utils.utils as utils


class VigenereSolver:

    def __init__(self):
        self.cipher = VigenereCipher()
        self.caesar_solver = CaesarSolver()
        self.scorer = Scorer()

    def solve(self, cipher_text: str, max_key_length: int = 20, top_n: int = 3) -> list[tuple[str, str, float]]:
        """
        Automated Vigenere Solver testing key lengths 1 to max_key_length,
        using letter-only streams to match VigenereCipher.
        """
        results = []
        letter_count = sum(char.isalpha() for char in cipher_text)

        for k in range(1, max_key_length + 1):
            if k >= letter_count:
                continue

            streams = ['' for _ in range(k)]
            letter_index = 0
            for char in cipher_text:
                if char.isalpha():
                    streams[letter_index % k] += char
                    letter_index += 1

            key_chars = []
            for stream in streams:
                if not stream:
                    key_chars.append('A')
                    continue

                caesar_results = self.caesar_solver.solve(stream, top_n=1)
                if caesar_results:
                    best_shift = caesar_results[0][0]
                    key_chars.append(utils.UPPER[best_shift])
                else:
                    key_chars.append('A')

            estimated_key = "".join(key_chars)
            plaintext = self.cipher.decrypt(cipher_text, estimated_key)

            score = self.scorer.score_text(plaintext)
            results.append((estimated_key, plaintext, score))

        results.sort(key=lambda x: x[2])
        return results[:top_n]
