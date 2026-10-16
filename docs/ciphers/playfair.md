# Playfair Cipher Module

An implementation of the Playfair Cipher, featuring a 5x5 key square, digraph-based substitution, modular arithmetic transformation rules, and automatic padding.

# Overview

Unlike standard substitution ciphers that encrypt single letters, the Playfair cipher encrypts pairs of letters (digraphs) simultaneously. Invented by Charles Wheatstone in 1854, it significantly increases resistance to traditional frequency analysis by transforming pairs of letters based on their geometric positions on a 5x5 key matrix

## Key Cipher Components

### 1. generate_matrix()
Takes a keyword, converts it to uppercase, replaces J and I, and strips duplicate letters. It then fills the remaining cell of a 5x5 grid sequentially with the rest of the alphabet.

### 2. process_text()
Cleans the input text by removing non-alphabetic characters and grouping letters into two-letter pairs (digraphs). If a pair contains identical consecutive letters e.g. "LL" then a filler letter (typically 'x') is inserted to break them up e.g. "LXL". An odd-length trailing letter also receives and X for padding.

### 3. _transform_pair()
Locates the coordinates (r,c) of both letters in the matrix and applies one of the three geometric rules using modular arithmetic (mod 5)

- Same Row: Shifts column indices right (for encryption) or left (for decryption) wrapping around the edges.
- Same Column: Shift row indices right (for encryption) or left (for decryption) wrapping around the edges.
- Rectangle Rule: Swaps the column coordinates of the two letters while keeping their row coordinates the same.

### 4. clean_text()
Post-Processes the decrypted text to automatically restore double letters from padding e.g. "SXS" → "SS" and strips any trailing padding 'X'.

## Limitations

### Ambiguity with I/J
Because the English alphabet has 26 letters and the grid only holds 25, I and J share a single cell, meaning decrypted text may occasionally require contextual interpretation for those letters

### Classic Cipher Weakness
While vastly superior to single-letter substitution, digraph frequencies can still be targeted by advanced cryptoanalysis compared to modern encryption standards.

## Basic Usage Example

```python
cipher = PlayfairCipher()

original_message = "Secret Message"
keyword = "Monarchy"

print(f"Original: {original_message}")

encrypted_message = cipher.encrypt(original_message, keyword)
print(f"Encrypted: {encrypted_message}")

decrypted_message = cipher.decrypt(encrypted_message, keyword)
print(f"Decrypted: {decrypted_message}")