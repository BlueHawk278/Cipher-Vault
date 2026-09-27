# Affine Cipher Solver

An implementation of an automated cryptanalysis solver designed to crack Affine ciphers by testing all valid key pairs and evaluating candidate decryptions using statistical metrics and n-gram language models.

---

## Overview

Unlike a simple Caesar cipher (which only has 26 possible shifts), the Affine cipher relies on a dual-key system $(a, b)$ where the multiplier $a$ must be coprime to 26. This creates 312 possible key combinations ($12 \text{ values of } a \times 26 \text{ values of } b$). The `AffineSolver` automates the decryption process by iterating through all valid key pairs, scoring each resulting plaintext using Chi-Squared statistics, n-gram log-probabilities, and an Index of Coincidence (IC) penalty, and ranking the top candidates.

---

## Mathematical Representation

### 1. Key Space Generation
The multiplier $a$ must share no common factors other than 1 with 26 ($\gcd(a, 26) = 1$), yielding 12 valid choices for $a$:
$$a \in \{1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25\}$$
With 26 possible values for $b$ ($0 \text{ to } 25$), the total search space consists of $12 \times 26 = 312$ unique key pairs.

### 2. Combined Scoring Function
The solver ranks candidate decryptions by combining three evaluation metrics:
$$\text{Combined Score} = \chi^2 - (S_{\text{ngram}} \times 0.1) + (\vert{}IC_{\text{calculated}} - 0.067\vert{} \times 100)$$
* **Chi-Squared ($\chi^2$):** Lower scores indicate a closer match to English letter frequencies.
* **N-Gram Log-Probability ($S_{\text{ngram}}$):** Higher scores indicate natural English letter clustering.
* **IC Penalty:** Penalizes deviations from the target English Index of Coincidence ($0.067$).

*Note: The combined score is sorted in ascending order so that the lowest total score represents the most accurate plaintext.*

---

## Key Component Details

### 1. `__init__()`
* **Action:** Initializes the Affine cipher instance, loads the Chi-Squared and IC calculators, and loads pre-calculated bigram, trigram, and quadgram JSON scoring models.

### 2. `solve()`
* **Action:** Generates all 312 valid $(a, b)$ key pairs, decrypts the ciphertext across every key pair, scores each result, sorts them in ascending order, and returns the top $N$ ranked candidates.

### 3. `generate_all_key_pairs()`
* **Action:** Computes valid $a$ values using `math.gcd(a, 26) == 1` and pairs them with every possible $b$ value from $0$ to $25$.

### 4. `score_text()` & `ic_test()`
* **Action:** Integrates Chi-Squared goodness-of-fit, weighted multi-order n-gram scoring, and an Index of Coincidence deviation penalty into a single optimization metric.

---

## Limitations

* **Corpus Dependency:** The solver relies on external JSON frequency files for bigrams, trigrams, and quadgrams. Missing dependencies or file paths will cause runtime interruptions.
* **Processing Overhead:** Testing 312 key combinations with multi-order n-gram scoring requires slightly more compute time than mono-shift ciphers like Caesar, though it remains extremely fast for modern processors.

---

## Basic Usage Example

```python
from ciphers.affine_solver import AffineSolver

# Initialize the automated Affine solver
solver = AffineSolver()

# Provide an encrypted ciphertext string
encrypted_message = "RSPEG XTSDE APHQU..."

# Get the top 3 most likely decrypted solutions
top_results = solver.solve(encrypted_message, top_n=3)

for rank, (key_a, key_b, score, decoded_text) in enumerate(top_results, 1):
    print(f"Rank {rank} | Key A: {key_a} | Key B: {key_b} | Score: {score:.4f}")
    print(f"Decoded Text:\n{decoded_text}\n")