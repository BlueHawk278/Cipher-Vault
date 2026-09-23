import utils.utils as utils

class MonoalphabeticCipher:

    def encrypt(self, plain_text: str, key: str) -> str:
        if len(set(key)) != 26 or not key.isalpha():
            raise ValueError("Key must contain all 26 unique alphabetical characters.")

        key_lower = key.lower()
        key_upper = key.upper()

        # Create translation tables for both lower and upper case
        lower_trans = str.maketrans(utils.LOWER, key_lower)
        upper_trans = str.maketrans(utils.UPPER, key_upper)

        return plain_text.translate(lower_trans).translate(upper_trans)

    def decrypt(self, cipher_text: str, key: str) -> str:
        if len(set(key)) != 26 or not key.isalpha():
            raise ValueError("Key must contain all 26 unique alphabetical characters.")

        key_lower = key.lower()
        key_upper = key.upper()

        # Create translation tables for both lower and upper case
        lower_trans = str.maketrans(key_lower, utils.LOWER)
        upper_trans = str.maketrans(key_upper, utils.UPPER)

        return cipher_text.translate(lower_trans).translate(upper_trans)