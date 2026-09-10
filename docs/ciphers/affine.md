# Affine Cipher Module

An implementation of the classic **Affine Cipher** technique, featuring character-case preservation, input validation, and secure coprimality verification.

---

## Overview

The Affine Cipher is a type of monoalphabetic **substitution cipher** that combines multiplication and addition to encrypt letters. It is a generalization of the Caesar Cipher; while a Caesar Cipher only shifts letters, the Affine Cipher first multiplies the letter's position by a constant and then applies a shift.

---

## Mathematical Representation

The cipher mathematically maps letters to integers from 0 to 25.

Let **x** be the integer value of a character, and the key consist of two integers, **(a, b)**.

### Encryption Function
The transformation formula multiplies and shifts characters **forward**:

<div align="center">
  <b>E<sub>(a,b)</sub>(x) = (a · x + b) mod 26</b>
</div>

### Decryption Function
The transformation formula reverses the shift and multiplies by the **modular multiplicative inverse** of a:

<div align="center">
  <b>D<sub>(a,b)</sub>(x) = a<sup>-1</sup> · (x - b) mod 26</b>
</div>

*Note: The notation a<sup>-1</sup> represents the modular multiplicative inverse of a modulo 26. It satisfies the condition (a · a<sup>-1</sup>) mod 26 = 1.*

---

## Key Component Details

### 1. The Key Pair `(a, b)`
* **Domain Restrictions for `a`:** The multiplier `a` **must** be coprime to 26 (meaning the greatest common divisor gcd(a, 26) = 1). The only valid options in a 26-letter alphabet are: `1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25`. If `a` shares a factor with 26, multiple letters will encrypt to the same ciphertext, making decryption impossible.
* **Domain Restrictions for `b`:** The shift value `b` can be any positive or negative whole integer. It is automatically normalized using `b % 26`.
* **The Caesar Relationship:** If `a = 1`, the Affine Cipher reduces exactly to a standard Caesar Cipher with a shift of `b`.

### 2. Encrypt
* **Action:** Iterates through string inputs, converting characters based on the linear transformation formula.
* **Preservation:** Non-alphabet characters are untouched. Case alignment is completely retained.

### 3. Decrypt
* **Action:** Calculates the modular inverse a<sup>-1</sup> (typically using the Extended Euclidean Algorithm) and solves for x to reverse the transformation sequence.

---

## Implementation Decisions

* **Strict Input Validation:** The constructor requires a key pair `(a, b)`. It explicitly validates that `isinstance(a, int)` and `isinstance(b, int)` are true (filtering out Booleans). It then checks the math; if the greatest common divisor does not equal `1`, a `ValueError` is raised immediately.
* **String Lookup Performance:** Rather than dealing heavily with raw ASCII `ord()` offsets, this module utilizes static lookup strings (`UPPER` and `LOWER`). This improves script readability and makes the lookup strategy highly intuitive for developer review.
* **Precedence Safety:** Formulas explicitly bundle operations like `(((a * UPPER.index(char)) + b) % 26)` inside strict mathematical parentheses to guarantee operations execute in the correct order, permanently avoiding edge-of-alphabet errors.

---

## Limitations

* **Low Security Threshold:** With only 12 valid choices for `a` and 26 valid choices for `b`, there are only 12 × 26 = 312 possible keys. It is incredibly trivial to break via brute-force cryptanalysis or frequency analysis, and should **never be deployed to secure sensitive or production data**.
* **Character Scope Constraints:** The layout safely preserves numbers, punctuations, and spaces, but it **does not shift them**. Foreign alphabets, emojis, and special symbols fall outside the transformation loop.

---

## Basic Usage Example

```python
from ciphers.affine import AffineCipher

# We create an Affine cipher object with keys a=5 and b=8
# (5 is valid because greatest common divisor of 5 and 26 is 1)
cipher = AffineCipher(a=5, b=8)

original_message = "This is a secret message!"
print(f"Original:  {original_message}")

# Encrypt the message using: E(x) = (5x + 8) mod 26
encrypted_message = cipher.encrypt(original_message)
print(f"Encrypted: {encrypted_message}")
# Output: Rbgk gk a kieldr rdkkaid!

# Decrypt the message using: D(x) = 21 * (x - 8) mod 26
# (21 is the modular inverse of 5, since (5 * 21) % 26 == 1)
decrypted_message = cipher.decrypt(encrypted_message)
print(f"Decrypted: {decrypted_message}")
# Output: This is a secret message!
```
