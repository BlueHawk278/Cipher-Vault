UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"

class CaesarCipher:
    """Initialises the Caeser Cipher with a validated integer key"""

    def __init__(self, key: int):
        if not isinstance(key, int) or isinstance(key, bool):
            raise TypeError("Key must be a whole integer number.")

        # Key can only be from 0 to 25
        self.key = key % 26

    def encrypt(self, text: str) -> str:
        """Encrypts plain text by shifting letters forward by the key."""

        result = []
        for char in text:
            if char in UPPER:
                letter = ((UPPER.index(char) + self.key) % 26)
                result += UPPER[letter]
            elif char in LOWER:
                letter = ((LOWER.index(char) + self.key) % 26)
                result += LOWER[letter]
            else:
                # Keep spaces, punctuation, and numbers unchanged
                result.append(char)
        return "".join(result)

    def decrypt(self, text: str) -> str:
        """Decrypts cipher text by shifting letters backward by the key."""

        result = []
        for char in text:
            if char in UPPER:
                letter = ((UPPER.index(char) - self.key) % 26)
                result += UPPER[letter]
            elif char in LOWER:
                letter = ((LOWER.index(char) - self.key) % 26)
                result += LOWER[letter]
            else:
                result.append(char)
        return "".join(result)
