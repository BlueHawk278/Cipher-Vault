# Caesar Cipher Solver

An implementation of an automated cryptanalysis solver designed to crack Caesar ciphers without knowing the shift key by combining statistical goodness-of-fit testing with n-gram language model scoring.

---

## Overview

While a manual Caesar cipher decryption requires testing all 26 possible shifts and manually inspecting the text, the `CaesarSolver` automates this process. It generates all shift permutations, evaluates each candidate decryption using both **Chi-Squared statistics** and **weighted n-gram log-probabilities** (bigrams, trigrams, and quadgrams), and ranks the results to pinpoint the correct plaintext.

---

## Mathematical Representation

### 1. N-Gram Weighted Score
To leverage multiple language structures, individual n-gram scores are combined using a weighted average where longer sequences (quadgrams) receive higher confidence:
$$S_{\text{ngram}} = (S_{\text{bigram}} \times 0.1) + (S_{\text{trigram}} \times 0.3) + (S_{\text{quadgram}} \times 0.6)$$

### 2. Combined Optimization Score
The solver combines the Chi-Squared score ($\chi^2$, where lower is better) and the weighted n-gram log-probability score ($S_{\text{ngram}}$, where higher log-probability is better):
$$\text{Combined Score} = \chi^2 - (S_{\text{ngram}} \times 0.1)$$
*Note: The combined score is sorted in ascending order so that the lowest total score represents the most natural English text.*

---

## Key Component Details

### 1. `__init__()`
* **Action:** Initializes the Caesar cipher module, links the Chi-Squared calculator, and loads bigram, trigram, and quadgram JSON scoring datasets.

### 2. `solve()`
* **Action:** Generates all 26 shift variations, evaluates each through the scoring pipeline, sorts the results by score in ascending order, and returns the top $N$ ranked candidates.

### 3. `generate_all_shifts()`
* **Action:** Iterates through all 26 integer shifts to decrypt the ciphertext across every possible key space.

### 4. `score_text()` & `ngram_log_test()`
* **Action:** Computes hybrid evaluations by calculating the Chi-Squared statistical fit and merging weighted multi-order n-gram log probabilities.

---

## Limitations

* **Corpus Dependency:** The solver relies heavily on external JSON frequency files for bigrams, trigrams, and quadgrams. Missing file paths or corrupted datasets will cause runtime errors.
* **Text Length Sensitivity:** Very short ciphertexts lack the statistical sample size needed for reliable n-gram and Chi-Squared distributions, potentially resulting in incorrect top rankings.

---

## Basic Usage Example

```python
from ciphers.caesar_solver import CaesarSolver

# Initialize the automated solver
solver = CaesarSolver()

# Provide an encrypted ciphertext string
encrypted_message = "MAX YBKLM WHVNFXGMXW..."

# Get the top 3 most likely decrypted solutions
top_results = solver.solve(encrypted_message, top_n=3)

for rank, (shift, score, decoded_text) in enumerate(top_results, 1):
    print(f"Rank {rank} | Shift: {shift} | Score: {score:.4f}")
    print(f"Decoded: {decoded_text}\n")