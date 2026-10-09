import random
import utils.utils as utils
from analysis.n_gram_scorer import NGramScorer
from ciphers.monoalphabetic import MonoalphabeticCipher

class MonoalphabeticSolver:

    def __init__(self):
        self.cipher = MonoalphabeticCipher()

        self.bigram_scorer = NGramScorer('../../data/ngrams/english_bigrams.json', 2)
        self.trigram_scorer = NGramScorer('../../data/ngrams/english_trigrams.json', 3)
        self.quadgram_scorer = NGramScorer('../../data/ngrams/english_quadgrams.json', 4)

    def get_random_key(self):
        """Generates a random permutation of the alphabet."""
        alphabet = list(utils.UPPER)
        random.shuffle(alphabet)
        return "".join(alphabet)

    def fitness_func(self, text):
        """Tests how well the next decrypted text matches english n_gram patterns."""
        cleaned_text = "".join([char for char in text.upper() if char.isalpha()])

        return self.quadgram_scorer.score_text(cleaned_text)

    def solve(self, ciphertext: str, fitness_func, num_restarts=20, max_iterations=10000):
        """
        Runs hill climbing multiple times with different random starting keys
        to escape local maxima and find the global best solution.
        """
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

        return global_best_key, global_best_text, global_best_score

    def hill_climbing_solver(self, ciphertext: str, fitness_func=None, max_iterations=10000):
        """Solves the monoalphabetic substitution cipher using hill climbing with random restarts."""

        if fitness_func is None:
            fitness_func = self.fitness_func

        best_key = self.get_random_key()
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