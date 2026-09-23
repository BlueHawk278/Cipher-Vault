import utils.utils as utils

class CaesarCipher:

    def encrypt(self, plain_text: str, key: int) -> str:
        """Encrypts plain text by shifting letters forward by the key."""
        key = key % 26

        result = []
        for char in plain_text:
            if char in utils.UPPER:
                letter = ((utils.UPPER.index(char) + key) % 26)
                result += utils.UPPER[letter]
            elif char in utils.LOWER:
                letter = ((utils.LOWER.index(char) + key) % 26)
                result += utils.LOWER[letter]
            else:
                # Keep spaces, punctuation, and numbers unchanged
                result.append(char)
        return "".join(result)

    def decrypt(self, cipher_text: str, key: int) -> str:
        """Decrypts cipher text by shifting letters backward by the key."""
        key = key % 26

        result = []
        for char in cipher_text:
            if char in utils.UPPER:
                letter = ((utils.UPPER.index(char) - key) % 26)
                result += utils.UPPER[letter]
            elif char in utils.LOWER:
                letter = ((utils.LOWER.index(char) - key) % 26)
                result += utils.LOWER[letter]
            else:
                result.append(char)
        return "".join(result)
