# Vigenère Cipher Module

An implementation of the classic **Vigenère Cipher** technique, featuring polyalphabetic substitution, key extension handling, case preservation, and modular shift calculations.

---

## Overview

The Vigenère cipher is a method of encrypting alphabetic text by using a series of interwoven Caesar ciphers based on the letters of a keyword. Unlike monoalphabetic substitution ciphers (such as the standard Caesar cipher), the Vigenère cipher uses a repeating key to change the shift value for each character, making it significantly more secure against basic frequency analysis.

---

## Mathematical Representation

The cipher maps letters to integers from $0$ to $25$.

Let $x$ be the integer value of a character, and $k_i$ be the integer shift value derived from the corresponding key character at index $i$.

### Encryption Function
The shifting formula shifts characters **forward** based on the current key character:
$$E_k(x) = (x + k_i) \pmod{26}$$

### Decryption Function
The shifting formula shifts characters **backward** to recover the original text:
$$D_k(x) = (x - k_i) \pmod{26}$$

*Note: The modulo operator ($\pmod{26}$) ensures that shifts exceeding the boundaries of the alphabet securely wrap around.*

---

## Key Component Details

### 1. `__init__()`
* **Action:** Accepts a keyword string and normalizes it completely to uppercase to ensure predictable index lookups.

### 2. `encrypt()`
* **Action:** Dynamically generates an `extendedKey` matching the length of the plaintext by repeating the key as needed. It then iterates through each character, retrieves the corresponding shift value from the key, and applies a forward shift while preserving the character's original case. Non-alphabet characters remain untouched.

### 3. `decrypt()`
* **Action:** Reverses the encryption process by applying a backward shift using the extended key's corresponding characters.

---

## Limitations

* **Key Dependency:** The security of a Vigenère cipher relies heavily on the secrecy and length of the keyword. Short keys or repeating patterns can be analyzed using tools like Kasiski examination (see the Pattern Analyzer module).
* **Character Scope Constraints:** Non-alphabetical characters (spaces, punctuation, numbers) are preserved in the text string but are excluded from the shifting logic.

---

## Basic Usage Example

```python
from ciphers.vigenere import VigenereCipher

# Initialize the Vigenère cipher with a keyword
cipher = VigenereCipher("KEY")

original_message = "Hello, World!"
print(f"Original:  {original_message}")

# Encrypt the message using the key
encrypted_message = cipher.encrypt(original_message)
print(f"Encrypted: {encrypted_message}")

# Decrypt the message back to its original form
decrypted_message = cipher.decrypt(encrypted_message)
print(f"Decrypted: {decrypted_message}")