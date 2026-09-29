# Columnar Transposition Cipher Module

An implementation of a classic **Columnar Transposition Cipher**, featuring keyword-based column reordering, automatic padding, and grid-based text restructuring.

---

## Overview

Unlike substitution ciphers (which replace letters with other letters), a transposition cipher keeps the original letters intact but scrambles their positions. In a columnar transposition cipher, the plaintext is written out horizontally into a grid of a fixed width (determined by the keyword), and the columns are then read off in a specific order dictated by the alphabetical sequence of the keyword characters.

---

## Key Mechanism Details

### 1. `get_column_order()`
* **Action:** Takes the keyword string and returns a list of numerical indices representing the alphabetical sorting order of the key's characters.

### 2. `encrypt()`
* **Action:** Checks if the text length fits evenly into the number of columns. If not, it pads any remaining empty spaces with underscores (`_`). It then divides the text into rows, reorders the columns based on the key, and reads the columns vertically to produce the ciphertext.

### 3. `decrypt()`
* **Action:** Calculates grid dimensions from the ciphertext length and keyword size, reconstructs the grid column-by-column using the key's sort order, reads the rows horizontally back into normal text order, and strips any trailing padding underscores (`_`).

---

## Limitations

* **Padding Artifacts:** The use of padding characters (`_`) to fill incomplete final rows can occasionally reveal information about the exact length or structure of the original message.
* **Cipher Type Weakness:** Pure transposition ciphers preserve the exact letter frequencies of standard English. When used alone, they are vulnerable to anagramming tools and pattern analysis.

---

## Basic Usage Example

```python
from ciphers.columnar_transposition import ColumnarTransposition

# Initialize the columnar transposition cipher
cipher = ColumnarTransposition()

original_message = "SECUREMESSAGE"
keyword = "CIPHER"

print(f"Original:  {original_message}")

# Encrypt the message using the keyword
encrypted_message = cipher.encrypt(original_message, keyword)
print(f"Encrypted: {encrypted_message}")

# Decrypt the message back to its original form
decrypted_message = cipher.decrypt(encrypted_message, keyword)
print(f"Decrypted: {decrypted_message}")