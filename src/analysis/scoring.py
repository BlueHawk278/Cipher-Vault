from analysis.chi_squared_calculator import Chi_Squared_Calculator
from analysis.ic_calculator import IC_Calculator
from analysis.n_gram_scorer import NGramScorer

class Scorer:

    def __init__(self):
        self.chi_squared_calculator = Chi_Squared_Calculator()
        self.ic_calculator = IC_Calculator()

        self.bigram_scorer = NGramScorer('data/ngrams/english_bigrams.json', 2)
        self.trigram_scorer = NGramScorer('data/ngrams/english_trigrams.json', 3)
        self.quadgram_scorer = NGramScorer('data/ngrams/english_quadgrams.json', 4)

    def score_text(self, text: str) -> float:
        """Scores the text combining chi-squared, n-grams, and Index of Coincidence."""
        chi_score = self.chi_squared_test(text)
        ngram_score = self.ngram_log_test(text)
        ic_score = self.ic_test(text)

        target_ic = 0.067
        ic_penalty = abs(ic_score - target_ic)

        combined_score = chi_score - (ngram_score * 0.1) - (ic_penalty * 100)

        return combined_score

    def chi_squared_test(self, text: str) -> float:
        return self.chi_squared_calculator.calculate_score(text)

    def ic_test(self, text: str) -> float:
        return self.ic_calculator.calculate_ic(text)

    def ngram_log_test(self, text: str) -> float:
        bigram_score = self.bigram_scorer.score_text(text)
        trigram_score = self.trigram_scorer.score_text(text)
        quadgram_score = self.quadgram_scorer.score_text(text)

        weighted_score = (bigram_score * 0.1) + (trigram_score * 0.3) + (quadgram_score * 0.6)
        return weighted_score