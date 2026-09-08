# Caesar Cipher Module

An implementation of the classic **Caesar Cipher** technique, featuring character-case preservation, input validation, and secure alphabet wrap-around handling.

---

## Overview

The Caesar Cipher is one of the earliest and simplest known encryption techniques. It is a type of **substitution cipher** where each letter in the plaintext is shifted down the alphabet by a fixed number of positions.

---

## Mathematical Representation

The cipher mathematically maps letters to integers from \(0\) to \(25\).

Let \(x\) be the integer value of a character, and \(k\) be the transformation key.

### Encryption Function
The shifting formula shifts characters **forward**:
\[E_k(x) = (x + k) \pmod{26}\]

### Decryption Function
The shifting formula shifts characters **backward**:
\[D_k(x) = (x - k) \pmod{26}\]

*Note: The modulo operator (\(\pmod{26}\)) ensures that shifts exceeding the boundaries of the alphabet securely wrap around back to the beginning.*

---

## Key Component Details

### 1. The Key
* **Domain:** Accepts any positive or negative whole integer.
* **Normalisation:** The key is automatically simplified using `key % 26`. For example, a key of `28` is cleanly normalized to `2`, and `-3` automatically normalises to `23`.

### 2. Encrypt
* **Action:** Iterates through string inputs, converting characters based on the forward shift formula.
* **Preservation:** Non-alphabet characters are untouched. Case alignment is completely retained.

### 3. Decrypt
* **Action:** Reverses the exact transformation sequence of the encryption method by shifting backward using the subtraction math block.

---

## Implementation Decisions

* **Strict Input Validation:** To eliminate runtime anomalies, the constructor checks keys using `isinstance(key, int)`. It explicitly filters out Booleans (which inherit from integers in Python) to guarantee an integer is provided.
* **String Lookup Performance:** Rather than dealing heavily with raw ASCII `ord()` offsets, this module utilizes static lookup strings (`UPPER` and `LOWER`). This improves script readability and makes the lookup strategy highly intuitive for developer review.
* **Precedence Safety:** Formulas explicitly bundle operations like `((UPPER.index(char) + self.key) % 26)` inside strict mathematical parentheses. This forces addition/subtraction to execute *before* the modulo operation, permanently avoiding `IndexError` exceptions on alphabet edges (`X`, `Y`, `Z`).

---

## Limitations

* **Low Security Threshold:** Because the alphabet only contains 26 possible shifting patterns, a Caesar cipher is highly vulnerable to brute-force cryptanalysis. It should only be deployed for educational, debugging, or obfuscation goals—**never for securing sensitive or production data**.
* **Character Scope Constraints:** The layout safely preserves numbers, punctuations, and spaces, but it **does not shift them**. Foreign alphabets, emojis, and special symbols fall outside the transformation loop.

---

## Basic Usage Example

```python
from src.cipher_toolkit.ciphers.caesar import CaesarCipher

# We create a cipher object with a key of 5
cipher = CaesarCipher(5)

original_message = "This is a secret message!"
print(f"Original:  {original_message}")

# When shifted forward by 5, the original message becomes:
encrypted_message = cipher.encrypt(original_message)
print(f"Encrypted: {encrypted_message}")
# Output: Ymnx nx f xjhwjy rjxxflj!

# When shifted back by 5, the encrypted message returns to its original form:
decrypted_message = cipher.decrypt(encrypted_message)
print(f"Decrypted: {decrypted_message}")
# Output: This is a secret message!
```
