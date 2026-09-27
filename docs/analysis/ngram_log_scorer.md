# N-Gram Log Scorer

An implementation of an n-gram language model scorer used in cryptanalysis to evaluate how "English-like" a candidate plaintext is by utilizing log-probabilities.

---

## Overview

When automatically cracking ciphers (such as substitution or transposition ciphers) using optimization algorithms like hill-climbing, the system needs a way to score candidate decryptions. The `NGramScorer` evaluates text by checking overlapping letter sequences against a pre-calculated frequency dataset, assigning higher aggregate scores to text that mirrors natural English patterns.

---

## Mathematical Representation

Let $C$ be the count of a specific n-gram, and $N$ be the total count of all n-grams in the training corpus.

### 1. Probability Calculation
The probability $P(\text{ngram})$ of an n-gram occurring is:
$$P(\text{ngram}) = \frac{C}{N}$$

### 2. Log-Probability Transformation
To prevent underflow issues from multiplying many small decimal probabilities together, probabilities are converted into base-10 logarithms:
$$\text{Score}(\text{ngram}) = \log_{10}\left(\frac{C}{N}\right)$$

### 3. Total Text Score
The final score of a text of length $L$ with window size $n$ is the sum of the log-probabilities of each overlapping n-gram:
$$\text{Total Score} = \sum_{i=0}^{L - n} \text{Score}(\text{ngram}_i)$$

*Note: If an n-gram is missing from the pre-loaded dataset, a default floor score (derived from a pseudo-count of 0.01) is assigned to penalize unnatural letter combinations.*

---

## Key Component Details

### 1. `__init__()`
* **Action:** Initializes the scorer with a target n-gram size and file path, automatically triggering the data loader.

### 2. `load_data()`
* **Action:** Reads raw n-gram counts from a JSON file, computes total corpus volume, converts counts into $\log_{10}$ probabilities, and establishes a safe floor score for unseen sequences.

### 3. `score_text()`
* **Action:** Normalizes the candidate text using the `Frequency` formatter, checks text length against the n-gram size, slides an overlapping window across the text, and accumulates the total log probability score.

---

## Limitations

* **Dataset Dependency:** The accuracy of the scorer depends entirely on the quality and size of the external JSON frequency dataset (e.g., standard English 3-gram or 4-gram corpora).
* **Length Bias:** Shorter texts yield fewer overlapping n-grams, resulting in lower cumulative scores that require careful baseline comparisons.

---

## Basic Usage Example

```python
from analysis.ngram_scorer import NGramScorer

# Initialize the scorer with an n-gram frequency JSON file (e.g., 3-grams)
scorer = NGramScorer("path/to/ngrams_3gram.json", n=3)

# Evaluate a candidate plaintext
candidate_text = "This is a test message for cryptanalysis."
score = scorer.score_text(candidate_text)

print(f"Log-probability score: {score}")