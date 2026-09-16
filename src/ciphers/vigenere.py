import utils.utils as utils

class VigenereCipher:

    def __init__(self, key: str) -> None:
        # Save the key entirely in uppercase to make index lookups predictable
        self.key = key.upper()
        self.extendedKey = None

    def encrypt(self, plain_text: str) -> str:
        self.extendedKey = (self.key * len(plain_text))[: len(plain_text)]
        result = []

        for i in range(len(plain_text)):
            char = plain_text[i]
            key_char = self.extendedKey[i]

            shift = utils.UPPER.index(key_char)

            if char in utils.UPPER:
                letter = (utils.UPPER.index(char) + shift) % 26
                result.append(utils.UPPER[letter])
            elif char in utils.LOWER:
                letter = (utils.LOWER.index(char) + shift) % 26
                result.append(utils.LOWER[letter])
            else:
                result.append(char)
        return "".join(result)

    def decrypt(self, cipher_text: str) -> str:
        self.extendedKey = (self.key * len(cipher_text))[: len(cipher_text)]
        result = []

        for i in range(len(cipher_text)):
            char = cipher_text[i]
            key_char = self.extendedKey[i]

            shift = utils.UPPER.index(key_char)

            if char in utils.UPPER:
                letter = (utils.UPPER.index(char) - shift) % 26
                result.append(utils.UPPER[letter])
            elif char in utils.LOWER:
                letter = (utils.LOWER.index(char) - shift) % 26
                result.append(utils.LOWER[letter])
            else:
                result.append(char)
        return "".join(result)
