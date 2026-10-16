import random
import utils.utils as utils
from analysis.n_gram_scorer import NGramScorer
from ciphers.monoalphabetic import MonoalphabeticCipher
from collections import Counter

class MonoalphabeticSolver:

    def __init__(self):
        self.cipher = MonoalphabeticCipher()

        self.bigram_scorer = NGramScorer('data/ngrams/english_bigrams.json', 2)
        self.trigram_scorer = NGramScorer('data/ngrams/english_trigrams.json', 3)
        self.quadgram_scorer = NGramScorer('data/ngrams/english_quadgrams.json', 4)

        with open('../../data/common_words.txt', 'r') as f:
            self.dictionary = set(word.strip().upper() for word in f)

    def dictionary_fitness_bonus(self, text: str) -> float:
        """
        Evaluates dictionary word matches with strict minimum lengths
        and a low weight to prevent overlapping substring inflation.
        """
        cleaned = "".join(text.upper().split())
        if not cleaned:
            return 0.0

        score = 0.0
        word_len = len(cleaned)

        i = 0
        while i < word_len:
            matched = False
            # Require words to be at least 3 characters long (i + 3) to avoid 2-letter noise
            for j in range(min(word_len, i + 12), i + 3, -1):
                candidate = cleaned[i:j]
                if candidate in self.dictionary:
                    # Light multiplier (0.5) to break ties without overpowering n-grams
                    score += len(candidate) * 0.5
                    i = j
                    matched = True
                    break
            if not matched:
                i += 1

        return score

    def get_frequency_seeded_key(self, ciphertext: str):
        """Generates an initial key based on monogram frequency analysis."""
        english_freq = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

        cleaned = "".join([char for char in ciphertext.upper() if char.isalpha()])
        counts = Counter(cleaned)
        sorted_cipher_letters = [char for char, count in counts.most_common()]

        all_letters = list(utils.UPPER)
        remaining_letters = sorted([char for char in all_letters if char not in sorted_cipher_letters])

        cipher_alphabet_order = sorted_cipher_letters + remaining_letters

        # Map ciphertext frequency order to English frequency order
        key_mapping = {}
        for cipher_char, english_char in zip(cipher_alphabet_order, english_freq):
            key_mapping[cipher_char] = english_char

        # Build the final 26-character key aligned with standard A-Z plaintext order
        final_key = []
        for standard_char in utils.UPPER:
            # Find what ciphertext character maps to this standard char, or default
            mapped = next((c for c, e in key_mapping.items() if e == standard_char), standard_char)
            final_key.append(mapped)

        return "".join(final_key)

    def refine_key(self, ciphertext: str, key: str, fitness_func) -> tuple[str, str, float]:
        """
        Exhaustively tests all 325 possible pairwise character swaps on the best key
        found so far. If any single swap improves the fitness score, it updates the key
        and repeats until no further single-swap improvements can be found.
        """
        best_key = key
        best_text = self.cipher.decrypt(ciphertext, best_key)
        best_score = fitness_func(best_text)

        improved = True
        while improved:
            improved = False
            key_list = list(best_key)

            # Check all pairs of alphabet positions (26 * 25 / 2 = 325 combinations)
            for i in range(26):
                for j in range(i + 1, 26):
                    # Swap two characters in the key
                    key_list[i], key_list[j] = key_list[j], key_list[i]
                    test_key = "".join(key_list)

                    test_text = self.cipher.decrypt(ciphertext, test_key)
                    test_score = fitness_func(test_text)

                    if test_score > best_score:
                        best_score = test_score
                        best_key = test_key
                        best_text = test_text
                        improved = True
                        break  # Break inner loops and restart search with new best key
                    else:
                        # Revert the swap if it didn't improve the score
                        key_list[i], key_list[j] = key_list[j], key_list[i]
                if improved:
                    break

        return best_key, best_text, best_score

    def fitness_func(self, text: str) -> float:
        """Tests how well the decrypted text matches English patterns and lipogram constraints."""
        cleaned_text = "".join([char for char in text.upper() if char.isalpha()])
        if not cleaned_text:
            return -99999.0

        # 1. Calculate standard N-gram scores
        bi_score = self.bigram_scorer.score_text(cleaned_text)
        tri_score = self.trigram_scorer.score_text(cleaned_text)
        quad_score = self.quadgram_scorer.score_text(cleaned_text)

        ngram_score = (bi_score * 0.1) + (tri_score * 0.3) + (quad_score * 0.6)

        # 2. Character Frequency Penalties (The Low-E Trick Detector)
        char_penalty = 0.0
        text_length = len(cleaned_text)

        e_count = cleaned_text.count('E')
        e_frequency = e_count / text_length if text_length > 0 else 0

        # If 'E' appears at an unnaturally low frequency (between 0% and 6%),
        # it's the solver trying to cheat on a lipogram.
        # 0% (lipogram) and >6% (normal English) are both safe.
        if 0 < e_frequency < 0.06:
            char_penalty += 100000.0

        # 3. Dictionary bonus (with safe 0.5 weight and min length 3)
        word_bonus = self.dictionary_fitness_bonus(text)

        return ngram_score + word_bonus - char_penalty

    def solve(self, ciphertext: str, fitness_func, num_restarts=25, max_iterations=10000):
        global_best_key = None
        global_best_text = None
        global_best_score = float('-inf')

        for run in range(num_restarts):
            key, text, score = self.hill_climbing_solver(ciphertext, fitness_func, max_iterations)

            if score > global_best_score:
                global_best_score = score
                global_best_key = key
                global_best_text = text
                print(f"Restart {run + 1}/{num_restarts} -> Score: {score:.2f} ✓ New best!")
            else:
                print(f"Restart {run + 1}/{num_restarts} -> Score: {score:.2f}")

        # --- NEW: Final Polish Pass ---
        print("Running key refinement polish...")
        global_best_key, global_best_text, global_best_score = self.refine_key(
            ciphertext, global_best_key, fitness_func
        )

        return global_best_key, global_best_text, global_best_score

    def hill_climbing_solver(self, ciphertext: str, fitness_func=None, max_iterations=10000):
        """Solves the monoalphabetic substitution cipher using hill climbing with random restarts."""

        if fitness_func is None:
            fitness_func = self.fitness_func

        best_key = self.get_frequency_seeded_key(ciphertext)
        best_text = self.cipher.decrypt(ciphertext, best_key)
        best_score = fitness_func(best_text)

        stagnation_limit = 1000  # Increased from 500
        stagnations = 0

        for iteration in range(max_iterations):
            # Create a neighbor key by swapping two random characters
            key_list = list(best_key)
            index1, index2 = random.sample(range(26), 2)
            key_list[index1], key_list[index2] = key_list[index2], key_list[index1]
            new_key = "".join(key_list)

            # Test the new key
            new_text = self.cipher.decrypt(ciphertext, new_key)
            new_score = fitness_func(new_text)

            # Accept if better, or with small probability to escape local maxima
            if new_score > best_score:
                best_key = new_key
                best_score = new_score
                best_text = new_text
                stagnations = 0
            else:
                stagnations += 1

            # If stagnant, try larger moves (swap 3 characters occasionally)
            if stagnations > stagnation_limit // 2 and stagnations % 50 == 0:
                # Make a bigger move by swapping 3 random positions
                key_list = list(best_key)
                indices = random.sample(range(26), 3)
                key_list[indices[0]], key_list[indices[1]], key_list[indices[2]] = (
                    key_list[indices[2]], key_list[indices[0]], key_list[indices[1]]
                )
                escape_key = "".join(key_list)
                escape_text = self.cipher.decrypt(ciphertext, escape_key)
                escape_score = fitness_func(escape_text)

                if escape_score > best_score:
                    best_key = escape_key
                    best_score = escape_score
                    best_text = escape_text
                    stagnations = 0

            if stagnations >= stagnation_limit:
                break

        return best_key, best_text, best_score


if __name__ == "__main__":
    solver = MonoalphabeticSolver()
    ciphertext = "AKLKH JKHNB YBAHB AIAVA IXELB JHEJH KZVUE XTEXL AXIZK FVUEX IYBNB AJNAH\nJBAJN YFIEH BEHJB YKLBJ JBAJF AXJBF YKLBW QVFAE XAUUX ELBJJ BAJEI EYJEO\nNYFIJ BAJNA HAUNA QHRKH JAXEX OBYFJ NYYKJ YGWQL FAHZG YNUYF GYKUA NYFIN\nBEOBV QAHHY OEAJE YXVFY KLBJE XJYZU AQAXE XOYXL FKYKH WAHHY GXYKX HEIEY\nWHHUY LAXHA XIHAQ EXLHA OYXGK HEXLA WYFZB YKHYK JZYKF EXLNB EOBEH YKLBJ\nEXMAE XJYOY XJFYU YFJKF XYGGV KJNBE OBNYK XIAFY KXIWQ WEXIA NBEFU NEXIY\nGAOYF IANBE ZUAHB YGAOY FIAOY FIJBA JNYKU IHZUE JALAE XAXIA LAEXN YKUIT\nXEJAL AEXAX IALAE XYGNY FIHNE JBYKJ OYWWK XEOAJ EYXYF AXQZY HHEVE UEJQY\nGOYWV EXAJE YXNYF IHNEJ BYKJZ FYXKX OEAJE YXHEL XEGEO AJEYX YFJFA XHOFE\nZJEYX VKJYK JYGNB EOBXY JNEJB HJAXI EXLNA HVFYK LBJGY FJBAG UKPAO YXJEX\nKYKHO YWZAO JAXIU KOEIG UYNAX EXJKE JEYXA MAOEU UAJEX LGFEH HYXYG EUUKW\nEXAJE YXAHE GOAKL BJEXA GUAHB YGUEL BJXEX LYFEX AWEHJ AVFKZ JUQFE HEXLJ\nYKXHB FYKIA XYVME YKHHE LXVKJ AHELX AUAHJ BAJNY KUIUA HJAXE XHJAX JYXUQ\nJYMAX EHBGY FLYYI\n"
    best_key, decrypted_text, score = solver.solve(
        ciphertext, fitness_func=solver.fitness_func, num_restarts=25, max_iterations=10000
    )
    print("\n--- Final Decryption Result ---")
    print(f"Key: {best_key}")
    print(f"Score: {score}")
    print(f"Text:\n{decrypted_text}")