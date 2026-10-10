from pathlib import Path
import json
import math


class NGramScorer:
    def __init__(self, filepath, n):
        self.n = n
        self.ngram_scores = {}
        self.floor_score = 0.0
        self.load_data(filepath)

    def load_data(self, filepath):
        """Loads frequency data from JSON and converts to log10 probabilities safely."""
        project_root = Path(__file__).resolve().parents[2]
        target_path = (project_root / filepath).resolve()

        with open(target_path, 'r') as f:
            raw_data = json.load(f)

        total_count = sum(raw_data.values())

        self.ngram_scores = {
            ngram.upper(): math.log10(count / total_count)
            for ngram, count in raw_data.items()
        }

        min_prob = 0.01 / total_count
        self.floor_score = math.log10(min_prob)

    def score_text(self, text):
        """Evaluates a candidate text using overlapping n-gram probabilities."""
        score = 0.0

        if len(text) < self.n:
            return self.floor_score * len(text)

        for i in range(len(text) - self.n + 1):
            ngram = text[i:i + self.n].upper()
            score += self.ngram_scores.get(ngram, self.floor_score)

        return score