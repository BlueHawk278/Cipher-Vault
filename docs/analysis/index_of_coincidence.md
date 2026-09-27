# Index of Coincidence (IC)

An implementation of the Index of Coincidence calculator used in cryptanalysis to measure letter repetition rates within text.

---

## Overview

The Index of Coincidence (IC) measures the probability that two randomly selected letters from a given text will be the same. It is a powerful statistical tool used to:
* Determine whether a ciphertext has been encrypted using a monoalphabetic substitution cipher (like Caesar) or a polyalphabetic substitution cipher (like Vigenère).
* Estimate the key length of polyalphabetic ciphers.

---

## Mathematical Representation

Let $N$ be the total number of letters, and $n_i$ be the count of each individual letter (from $A$ to $Z$).

### Index of Coincidence Formula
$$IC = \frac{\sum_{i=1}^{26} n_i(n_i - 1)}{N(N - 1)}$$

*Note: In natural English text, the IC is approximately $0.0667$, whereas random uniform text yields an IC closer to $0.0385$.*

---

## Key Component Details

### 1. `calculate_ic()`
* **Action:** Retrieves letter counts, filters out zero-count elements to clean the dictionary, computes the numerator and denominator, and returns the final float ratio.

### 2. `get_numerator()`
* **Action:** Iterates through letter counts to compute $\sum n_i(n_i - 1)$, representing total matching letter pairs.

### 3. `get_denominator()`
* **Action:** Computes $N(N - 1)$, representing total possible letter pairs in the text.

---

## Limitations

* **Text Length Dependency:** IC calculations require sufficient text volume. Short phrases or sentences exhibit high statistical variance, making reliable analysis difficult.

---

## Basic Usage Example

```python
from analysis.statistics import ic_calculator

# Initialize the IC calculator
ic_calc = ic_calculator()

cipher_text = "Vwkhu lv d vhfuhw phvvdjh!"
ic_score = ic_calc.calculate_ic(cipher_text)

print(f"Index of Coincidence: {ic_score}")