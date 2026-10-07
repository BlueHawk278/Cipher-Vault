import numpy as np
from utils.utils import normalize, UPPER

class HillCipher:

    def encrypt(self, plaintext, key: np.ndarray):
        plaintext = normalize(plaintext)
        n = key.shape[0]
        modulus = len(UPPER)

        # Pad plaintext with 'X' if its length isn't a multiple of n
        if len(plaintext) % n != 0:
            plaintext += 'X' * (n - len(plaintext) % n)

        ciphertext = ""

        for i in range(0, len(plaintext), n):
            chunk = [UPPER.index(c) for c in plaintext[i:i+n]]
            vector = np.array(chunk).reshape(n, 1)

            # Use modulus instead of hardcoded 26
            result = np.dot(key, vector) % modulus

            # Use val instead of i for clarity
            ciphertext += "".join(UPPER[int(val)] for val in result.flatten())

        return ciphertext

    def decrypt(self, ciphertext, key: np.ndarray):
        ciphertext = normalize(ciphertext)
        n = key.shape[0]
        modulus = len(UPPER)

        inv_key = self.mod_inverse_matrix(key, modulus)

        plaintext = ""
        for i in range(0, len(ciphertext), n):
            chunk = [UPPER.index(c) for c in ciphertext[i:i + n]]
            vector = np.array(chunk).reshape(n, 1)

            result = np.dot(inv_key, vector) % modulus
            plaintext += "".join(UPPER[int(val)] for val in result.flatten())

        # Strip trailing padding X's
        return plaintext.rstrip('X')

    def mod_inverse_matrix(self, matrix, modulus):
        det = int(round(np.linalg.det(matrix)))
        det_inv = self.mod_inverse(det % modulus, modulus)

        if det_inv is None:
            raise ValueError("Matrix is not invertible modulo the alphabet size.")

        n = matrix.shape[0]
        if n == 2:
            adjugate = np.array([[matrix[1, 1], -matrix[0, 1]], [-matrix[1, 0], matrix[0, 0]]])
            return (det_inv * adjugate) % modulus

        elif n == 3:
            adjugate = np.zeros((3, 3), dtype=int)
            for i in range(3):
                for j in range(3):
                    sub = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                    cofactor = ((-1) ** (i + j)) * int(round(np.linalg.det(sub)))
                    adjugate[j, i] = cofactor
            return (det_inv * adjugate) % modulus

        else:
            raise NotImplementedError("Only 2x2 and 3x3 matrices are supported.")

    def mod_inverse(self, a, modulus):
        a = a % modulus
        for x in range(1, modulus):
            if (a * x) % modulus == 1:
                return x
        return None

# 1. Instantiate the cipher
cipher = HillCipher()

# 2. Define a 2x2 key matrix (ensure its determinant is coprime with 26)
# Det of [[3, 3], [2, 5]] is (3*5) - (3*2) = 15 - 6 = 9.
# 9 mod 26 is 9, and 9 has a modular inverse mod 26 (which is 3).
key = np.array([[3, 3],
                [2, 5]])

# 3. Test text
plaintext = "HELLOHILL"

# 4. Encrypt
ciphertext = cipher.encrypt(plaintext, key)
print(f"Plaintext:  {plaintext}")
print(f"Ciphertext: {ciphertext}")

# 5. Decrypt
decrypted_text = cipher.decrypt(ciphertext, key)
print(f"Decrypted:  {decrypted_text}")