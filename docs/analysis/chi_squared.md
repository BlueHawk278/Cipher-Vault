### Chi-Squared Calculator

# Chi-Squared ($\chi^2$) Calculator Module

An implementation of the Chi-Squared goodness-of-fit statistical test used to evaluate how closely a candidate text matches natural English letter distributions.

---

## Overview

In cryptanalysis, when attempting to brute-force a substitution cipher (such as shifting through all 26 possible keys of a Caesar cipher), the correct decryption key will yield text whose letter frequencies closely mirror standard English. The Chi-Squared test automates this evaluation by scoring how closely observed frequencies match expected baseline values.

---

## Mathematical Representation

Let $N$ be the total number of letters, $O_i$ be the observed frequency count of a letter, and $E_i$ be the expected frequency count of that letter in standard English.

### Chi-Squared Formula
$$\chi^2 = N \sum_{i} \frac{(O_i - E_i)^2}{E_i}$$

*Note: A lower Chi-Squared score indicates a closer statistical match to standard English text.*

---

## Key Component Details

### 1. `__init__()`
* **Action:** Accepts the ciphertext, formats and normalizes it, calculates observed letter frequencies, and loads standard English expected frequencies alongside the total letter count.

### 2. `calculate_score()`
* **Action:** Iterates through every letter in the expected frequency dictionary, calculates squared differences between observed and expected rates, and scales the final sum by the total letter count.

---

## Limitations

* **Sample Size Sensitivity:** Short texts lack sufficient character diversity, resulting in noisy scores that can misidentify correct plaintexts.
* **Language Profile:** The module assumes standard English letter frequencies; encrypted text originating from other languages requires alternative frequency distributions.

---

## Basic Usage Example

```python
from analysis.statistics import chi_squared_calculator

# Initialize the Chi-Squared calculator with ciphertext
cipher_text = "Wklv lv d vhfuhw phvvdjh!"
chi_calc = chi_squared_calculator(cipher_text)

# Calculate the goodness-of-fit score
score = chi_calc.calculate_score()
print(f"Chi-Squared Score: {score}")