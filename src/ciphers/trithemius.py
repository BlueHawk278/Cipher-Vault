import utils.utils as utils

class TrithemiusCipher:

    def encrypt(self, plain_text: str, key: int) -> str:
        key = key % 26
        result = []
        letter_count = 0

        for char in plain_text:
            if char in utils.UPPER:
                letter = ((utils.UPPER.index(char) + key + letter_count) % 26)
                result.append(utils.UPPER[letter])
                letter_count += 1
            elif char in utils.LOWER:
                letter = ((utils.LOWER.index(char) + key + letter_count) % 26)
                result.append(utils.LOWER[letter])
                letter_count += 1
            else:
                result.append(char)
        return "".join(result)

    def decrypt(self, cipher_text: str, key: int) -> str:
        key = key % 26

        result = []
        letter_count = 0

        for i in range(len(cipher_text)):
            char = cipher_text[i]
            if char in utils.UPPER:
                letter = ((utils.UPPER.index(char) - key - letter_count) % 26)
                result.append(utils.UPPER[letter])
                letter_count += 1
            elif char in utils.LOWER:
                letter = ((utils.LOWER.index(char) - key - letter_count) % 26)
                result.append(utils.LOWER[letter])
                letter_count += 1
            else:
                result.append(char)
        return "".join(result)

trithemius = TrithemiusCipher()

print(trithemius.encrypt("Hello", 3))  # Example usage