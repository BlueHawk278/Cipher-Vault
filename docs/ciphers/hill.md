# Hill Cipher Module

An implementation of the Hill Cipher, featuring linear algebra-based polygraphic substitution, modular matrix inversion, automatic padding, and vector based chunk processing.

## Overview

Unlike traditional substitution ciphers, the Hill Cipher uses linear algebra to encrypt blocks of text simultaneously. Plaintext letters are converted to numerical vectors, multiplied by a secret square key matrix, and modulated by the alphabet size. This makes it significantly more resistant to simple frequency analysis than standard monoalphabetic substitution ciphers.

## Key Cipher Components

### encrypt()
Normalises the input tet and pads it with trailing 'X' characters if its length is not a multiple of the key matrix dimension(n). It splits the text into chunks of size n, converts them into numerical column vectors using an alphabet mapping, multiplies them by the key matrix, applies modulo arithmetic, and returns the resulting ciphertext string.

### decrypt()
Computes the modular inverse of the key matrix using the determinant and adjugate matrix methods. It processes ciphertext blocks through matrix multiplication with the inverse key, converts the numerical results back to letters, and strips any trailing padding 'X' characters.

### mod_inverse_matrix()
Handles 2x2 and 3x3 matrices by calculating the determinant, finding its modular inverse relative to the alphabet size, and computing the corresponding adjugate matrix. Raises an error if the matrix is not invertible modulo the alphabet size.

### mod_inverse()
Utilises modular arithmetic to find the multiplicative inverse of the determinant within the given modulus.

## Limitations

### Matrix Invertibility
- Not every square matrix can serve as a valid key. A key matrix must be invertible modulo the alphabet size (i.e its determinant must be coprime with the modulus(26))

### Linear Vulnerability
- While stronger than monoalphabetic ciphers, the Hill Cipher os vulnerable to know-plaintext attacks because linear equations can be solved using algebra if a portion of the plaintext and ciphertext is intercepted.

## Basic Usage Example

```python
cipher = HillCipher()

key = np.array([[3, 3],
                [2, 5]])

plaintext = "HELLOHILL"

print(f"Plaintext: {plaintext}")

ciphertext = cipher.encrypt(plaintext, key)
print(f"Ciphertext: {ciphertext}")

decrypted_text = cipher.decrypt(ciphertext, key)
print(f"Decrypted: {decrypted_text")