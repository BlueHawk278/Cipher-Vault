import utils.utils as utils
import math

class AffineCipher:

    def __init__(self, keyA, keyB):
        if not isinstance(keyA, int) or isinstance(keyA, bool):
            raise TypeError("Key must be a whole integer number.")

        if not isinstance(keyB, int) or isinstance(keyB, bool):
            raise TypeError("Key must be a whole integer number.")

        self.keyA = keyA % 26
        self.keyB = keyB % 26

        if math.gcd(keyA, 26) != 1:
            raise ValueError("KeyA must be coprime to 26 (gcd must be 1).")

        # Modular inverse of KeyA for decryption
        self.keyA_inv = pow(self.keyA, -1, 26)

    def encrypt(self, plain_text):
        result = []

        for char in plain_text:
            if char in utils.UPPER:
                x = utils.UPPER.find(char)
                new_index = (self.keyA * x + self.keyB) % 26
                result.append(utils.UPPER[new_index])
            elif char in utils.LOWER:
                x = utils.LOWER.find(char)
                new_index = (self.keyA * x + self.keyB) % 26
                result.append(utils.LOWER[new_index])
            else:
                result.append(char)
        return "".join(result)

    def decrypt(self, cipher_text):
        result = []

        for char in cipher_text:
            if char in utils.UPPER:
                y = utils.UPPER.find(char)
                new_index = (self.keyA_inv * (y - self.keyB)) % 26
                result.append(utils.UPPER[new_index])
            elif char in utils.LOWER:
                y = utils.LOWER.find(char)
                new_index = (self.keyA_inv * (y - self.keyB)) % 26
                result.append(utils.LOWER[new_index])
            else:
                result.append(char)
        return "".join(result)