import utils.utils as utils

class VigenereCipher:

    def __init__(self):
        self.extendedKey = None
        self.key = None

    def encrypt(self, plain_text: str, key: str) -> str:
        self._set_key(key)
        result = []
        key_index = 0

        for char in plain_text:
            if char in utils.UPPER:
                shift = utils.UPPER.index(self.key[key_index % len(self.key)])
                letter = (utils.UPPER.index(char) + shift) % 26
                result.append(utils.UPPER[letter])
                key_index += 1
            elif char in utils.LOWER:
                shift = utils.UPPER.index(self.key[key_index % len(self.key)])
                letter = (utils.LOWER.index(char) + shift) % 26
                result.append(utils.LOWER[letter])
                key_index += 1
            else:
                result.append(char)
        return "".join(result)

    def decrypt(self, cipher_text: str, key: str) -> str:
        self._set_key(key)
        result = []
        key_index = 0

        for char in cipher_text:
            if char in utils.UPPER:
                shift = utils.UPPER.index(self.key[key_index % len(self.key)])
                letter = (utils.UPPER.index(char) - shift) % 26
                result.append(utils.UPPER[letter])
                key_index += 1
            elif char in utils.LOWER:
                shift = utils.UPPER.index(self.key[key_index % len(self.key)])
                letter = (utils.LOWER.index(char) - shift) % 26
                result.append(utils.LOWER[letter])
                key_index += 1
            else:
                result.append(char)
        return "".join(result)

    def _set_key(self, key: str) -> None:
        normalized_key = key.upper()
        if not normalized_key or any(char not in utils.UPPER for char in normalized_key):
            raise ValueError("Vigenere keys must contain only letters")
        self.key = normalized_key
        self.extendedKey = None
