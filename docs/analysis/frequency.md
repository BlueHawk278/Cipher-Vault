# Frequency Analysis

An implementation of a letter frequency analysis tool designed to count, calculate decimal frequencies, and generate structured reports for cryptanalysis.

---

## Overview

Frequency analysis is the study of the frequency of letters or groups of letters in a ciphertext. Because different letters appear with characteristic frequencies in natural languages (such as English, where 'E' is the most common), frequency analysis is a powerful tool used to crack substitution ciphers like the Caesar cipher.

---

## Mathematical Representation

Let $N$ be the total number of valid alphabetical characters in the cleaned text, and $n_c$ be the count of a specific character $c$ (where $c$ belongs to the alphabet from $A$ to $Z$).

### Frequency Function
The decimal frequency $f(c)$ of any given letter is calculated as:
$$f(c) = \frac{n_c}{N}$$

*Note: If $N = 0$, the module gracefully handles the edge case to prevent division-by-zero errors, returning a frequency of $0.0$ for all letters.*

---

## Key Component Details

### 1. `format_text()`
* **Action:** Cleans the input string by converting all lowercase letters to uppercase and completely stripping out spaces, punctuation, and numbers. 
* **Purpose:** Ensures that only valid alphabetical characters are measured in the analysis.

### 2. `get_count()`
* **Action:** Pre-populates a dictionary with all uppercase letters mapped to `0`, then tallies the exact occurrences of each letter present in the cleaned ciphertext.

### 3. `get_freq()`
* **Action:** Converts raw letter counts into decimal ratios relative to the total character count $N$.

### 4. `display_count_and_frequency()`
* **Action:** Prints a clean, aligned text report showing the letter, its absolute count, and its decimal frequency formatted to 4 decimal places.

---

## Limitations

* **Character Scope Constraints:** Non-alphabetical characters (spaces, punctuation, numbers, and symbols) are stripped during formatting and are excluded from the frequency calculations.
* **Text Length Dependency:** Frequency analysis is most effective on longer blocks of text. Short ciphertexts may not accurately reflect standard language letter distributions.

---

## Basic Usage Example

```python
from analysis.frequency import Frequency

# Create a frequency analysis object
analyzer = Frequency("Uryyb jryqbhg!")

# Display the formatted count and frequency report
analyzer.display_count_and_frequency()

# Output shows counts and frequencies for all letters (with non-letters filtered out)