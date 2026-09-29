# Monoalphabetic Cipher Module

An implementation of a general **Monoalphabetic Substitution Cipher**, featuring custom alphabet key validation, case preservation, and fast string translation tables.

---

## Overview

A monoalphabetic substitution cipher is a substitution cipher where each letter in the plaintext is replaced with a corresponding ciphertext letter based on a fixed substitution alphabet (the key). Unlike the Caesar or Affine ciphers, which use mathematical formulas, a monoalphabetic cipher can use any arbitrary permutation of the 26-letter alphabet as its key, drastically increasing the key space ($26!$ possible combinations) but remaining vulnerable to frequency analysis.

---

## Key Mechanism Details

### 1. Key Validation
* **Condition:** The key must consist of exactly 26 unique alphabetical characters (`len(set(key)) == 26` and `key.isalpha()`). If invalid, a `ValueError` is raised.

### 2. `encrypt()`
* **Action:** Validates the key, normalizes it to both lowercase and uppercase, and builds Python translation tables using `str.maketrans()`. It maps both lowercase and uppercase plaintext letters to their corresponding cipher characters while leaving non-alphabetic symbols untouched.

### 3. `decrypt()`
* **Action:** Reverses the substitution mapping by swapping the source and destination alphabets in the translation tables, converting ciphertext back to the original plaintext.

---

## Limitations

* **Security Vulnerability:** Because each plaintext letter always maps to the exact same ciphertext letter, monoalphabetic ciphers are easily broken using frequency analysis, digram/trigram patterns, and language statistics.
* **Key Management:** Requires secure sharing or generation of a complete 26-character permutation key.

---

## Basic Usage Example

```python
from ciphers.monoalphabetic import MonoalphabeticCipher

# Initialize the cipher
cipher = MonoalphabeticCipher()

# Define a valid 26-character substitution key (permutation of the alphabet)
key = "QWERTYUIOPASDFGHJKLZXCVBNM"

original_message = "Hello, World!"
print(f"Original:  {original_message}")

# Encrypt the message
encrypted_message = cipher.encrypt(original_message, key)
print(f"Encrypted: {encrypted_message}")

# Decrypt the message back to its original form
decrypted_message = cipher.decrypt(encrypted_message, key)
print(f"Decrypted: {decrypted_message}")