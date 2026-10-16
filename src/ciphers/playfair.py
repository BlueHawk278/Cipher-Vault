import numpy as np
import re

class PlayfairCipher:

    def encrypt(self, plaintext, keyword):
        matrix = self.generate_matrix(keyword)
        digraphs = self.process_text(plaintext)
        ciphertext = []
        for pair in digraphs:
            ciphertext.append(self._transform_pair(matrix, pair, mode="encrypt"))
        return "".join(ciphertext)

    def decrypt(self, ciphertext, keyword):
        matrix = self.generate_matrix(keyword)
        digraphs = self.process_text(ciphertext)
        plaintext_raw = []
        for pair in digraphs:
            plaintext_raw.append(self._transform_pair(matrix, pair, mode="decrypt"))

        # Join the decrypted pairs back into a single string
        raw_text = "".join(plaintext_raw)

        # Clean up the filler X's
        return self.clean_text(raw_text)

    def clean_text(self, text):
        # 1. Replace sandwich patterns like 'SXS' back to 'SS'
        # This matches any letter, an 'X', and the exact same letter again
        cleaned = re.sub(r'([A-Z])X\1', r'\1\1', text)

        # 2. Optional: Remove a trailing 'X' if it was added as padding at the very end
        # (Only do this if you know your messages don't naturally end in X)
        if cleaned.endswith("X"):
            cleaned = cleaned[:-1]

        return cleaned

    def _transform_pair(self, matrix, pair, mode="encrypt"):
        r1, c1 = self.find_position(matrix, pair[0])
        r2, c2 = self.find_position(matrix, pair[1])

        shift = 1 if mode == "encrypt" else -1

        if r1 == r2:  # Same Row
          c1 = (c1 + shift) % 5
          c2 = (c2 + shift) % 5
        elif c1 == c2:  # Same Column
          r1 = (r1 + shift) % 5
          r2 = (r2 + shift) % 5
        else:  # Rectangle Rule
          c1, c2 = c2, c1

        return matrix[r1, c1] + matrix[r2, c2]

    def generate_matrix(self, keyword):
        keyword = keyword.upper().replace("J", "I")

        seen = set()
        matrix_chars = []
        for char in keyword + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
          if char.isalpha() and char not in seen:
            seen.add(char)
            matrix_chars.append(char)

        matrix_list = [
            matrix_chars[i : i + 5] for i in range(0, len(matrix_chars), 5)
        ]
        return np.array(matrix_list)

    def process_text(self, text):
        text = text.upper().replace("J", "I")
        text = "".join([c for c in text if c.isalpha()])

        digraphs = []
        i = 0
        while i < len(text):
          char1 = text[i]
          if i + 1 < len(text):
            char2 = text[i + 1]
            if char1 == char2:
              digraphs.append(char1 + "X")
              i += 1
            else:
              digraphs.append(char1 + char2)
              i += 2
          else:
            digraphs.append(char1 + "X")
            i += 1
        return digraphs

    def find_position(self, matrix, char):
        r, c = np.where(matrix == char)
        if len(r) > 0:
          return int(r[0]), int(c[0])
        return None

cipher = PlayfairCipher()

original_message = "Secret Message"
keyword = "Monarchy"

print(f"Original: {original_message}")

encrypted_message = cipher.encrypt(original_message, keyword)
print(f"Encrypted: {encrypted_message}")

decrypted_message = cipher.decrypt(encrypted_message, keyword)
print(f"Decrypted: {decrypted_message}")