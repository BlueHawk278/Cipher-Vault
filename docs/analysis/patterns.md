# Pattern Analyzer Module

An implementation of text pattern analysis tools, featuring n-gram extraction, position mapping, distance calculation, and Kasiski examination for estimating Vigenère cipher key lengths.

---

## Overview

Pattern analysis involves searching text for recurring sequences of characters (known as **n-grams**). By analyzing the distances between identical repeating n-grams, cryptanalysts can apply the **Kasiski examination** method to deduce the likely key length of polyalphabetic substitution ciphers like the Vigenère cipher.

---

## Key Component Details

### 1. `extract_ngrams()`
* **Action:** Iterates through a given text to extract sequential slices of length $n$.
* **Purpose:** Breaks down raw text strings into manageable sub-sequences for pattern matching.

### 2. `get_ngram_positions()`
* **Action:** Scans the text for n-grams of size $n$ and maps each unique sequence to a list of its starting index positions.

### 3. `get_ngram_distances()`
* **Action:** Computes the interval distances between consecutive occurrences of repeating n-grams based on their position indices.

### 4. `get_factors()`
* **Action:** Generates all integer factors (excluding 1) for a given distance number, which helps identify common divisors associated with potential key lengths.

### 5. `estimate_vigenere_key_length()`
* **Action:** Combines position mapping, distance calculation, and factor counting using a frequency counter (`Counter`) to output a ranked list of the most common potential key lengths within a specified range.

---

## Limitations

* **False Positives:** Random letter sequences can occasionally repeat by coincidence, producing misleading distance factors.
* **Text Length Dependency:** Kasiski examination requires sufficiently long ciphertexts containing multiple repeating sequences to yield accurate key length estimates.

---

## Basic Usage Example

```python
from analysis.pattern_analyzer import PatternAnalyzer

# Initialize the analyzer with a ciphertext
analyzer = PatternAnalyzer("ABCXYZABCXYZABC")

# Estimate the Vigenère key length using default 3-grams
key_length_estimates = analyzer.estimate_vigenere_key_length(analyzer.text, n=3, max_key_length=20)

print("Most likely key lengths:", key_length_estimates)