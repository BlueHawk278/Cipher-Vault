import utils.utils as utils

class CaesarCipher:
    """Initialises the Caesar Cipher with a validated integer key"""

    def __init__(self, key: int):
        if not isinstance(key, int) or isinstance(key, bool):
            raise TypeError("Key must be a whole integer number.")

        # Key can only be from 0 to 25
        self.key = key % 26

    def encrypt(self, plain_text: str) -> str:
        """Encrypts plain text by shifting letters forward by the key."""

        result = []
        for char in plain_text:
            if char in utils.UPPER:
                letter = ((utils.UPPER.index(char) + self.key) % 26)
                result += utils.UPPER[letter]
            elif char in utils.LOWER:
                letter = ((utils.LOWER.index(char) + self.key) % 26)
                result += utils.LOWER[letter]
            else:
                # Keep spaces, punctuation, and numbers unchanged
                result.append(char)
        return "".join(result)

    def decrypt(self, cipher_text: str) -> str:
        """Decrypts cipher text by shifting letters backward by the key."""

        result = []
        for char in cipher_text:
            if char in utils.UPPER:
                letter = ((utils.UPPER.index(char) - self.key) % 26)
                result += utils.UPPER[letter]
            elif char in utils.LOWER:
                letter = ((utils.LOWER.index(char) - self.key) % 26)
                result += utils.LOWER[letter]
            else:
                result.append(char)
        return "".join(result)
