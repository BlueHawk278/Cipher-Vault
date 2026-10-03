import utils.utils as utils
import math

class AffineCipher:

    def _validate_and_get_inverse(self, keyA: int, keyB: int):
        """Validates keys and calculates the modular inverse for keyA."""
        if not isinstance(keyA, int) or isinstance(keyA, bool):
            raise TypeError("KeyA must be a whole integer number.")
        if not isinstance(keyB, int) or isinstance(keyB, bool):
            raise TypeError("KeyB must be a whole integer number.")

        keyA = keyA % 26
        keyB = keyB % 26

        if math.gcd(keyA, 26) != 1:
            raise ValueError("KeyA must be coprime to 26 (gcd must be 1).")

        keyA_inv = pow(keyA, -1, 26)
        return keyA, keyB, keyA_inv

    def encrypt(self, plain_text: str, keyA: int, keyB: int) -> str:
        k_a, k_b, _ = self._validate_and_get_inverse(keyA, keyB)
        result = []

        for char in plain_text:
            if char in utils.UPPER:
                x = utils.UPPER.find(char)
                new_index = (k_a * x + k_b) % 26
                result.append(utils.UPPER[new_index])
            elif char in utils.LOWER:
                x = utils.LOWER.find(char)
                new_index = (k_a * x + k_b) % 26
                result.append(utils.LOWER[new_index])
            else:
                result.append(char)
        return "".join(result)

    def decrypt(self, cipher_text: str, keyA: int, keyB: int) -> str:
        k_a, k_b, k_a_inv = self._validate_and_get_inverse(keyA, keyB)
        result = []

        for char in cipher_text:
            if char in utils.UPPER:
                y = utils.UPPER.find(char)
                new_index = (k_a_inv * (y - k_b)) % 26
                result.append(utils.UPPER[new_index])
            elif char in utils.LOWER:
                y = utils.LOWER.find(char)
                new_index = (k_a_inv * (y - k_b)) % 26
                result.append(utils.LOWER[new_index])
            else:
                result.append(char)
        return "".join(result)