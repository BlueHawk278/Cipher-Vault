from pathlib import Path
import json
from typing import Any

from solvers.monoalphabetic_solver import MonoalphabeticSolver
import utils.utils as utils

class MonoalphabeticSolverTest:

    def __init__(self):
        self.solver = MonoalphabeticSolver()
        self.data = self.load_data()

    def load_data(self) -> Any | None:
        try:
            data_path = Path(__file__).resolve().parents[1] / "test_data.json"
            with data_path.open("r") as f:
                data = json.load(f)
                return data["monoalphabetic substitution"]
        except (OSError, KeyError, json.JSONDecodeError) as error:
            print(error)
            return None

    def run_tests(self):
        print("=" * 70)
        print("Starting Monoalphabetic Substitution Solver Tests")
        print("=" * 70)
        passed_count = 0
        failed_count = 0
        skipped_count = 0

        if not self.data:
            print("No test data available")
            return False

        for i, challenge in enumerate(self.data):
            key = challenge.get("key")
            pairs = [
                (name.removeprefix("ciphertext"), value)
                for name, value in challenge.items()
                if name.startswith("ciphertext") and isinstance(value, str)
            ]
            pairs = [
                (suffix, ciphertext, challenge.get(f"plaintext{suffix}"))
                for suffix, ciphertext in pairs
            ]
            if isinstance(challenge.get("ciphertext"), str):
                pairs = [("", challenge["ciphertext"], challenge.get("plaintext"))]

            if not isinstance(key, str) or not pairs or any(
                    not isinstance(plaintext, str) for _, _, plaintext in pairs
            ):
                print(f"\n[SKIP] Challenge #{i + 1} - Missing test data")
                skipped_count += 1
                continue

            print(f"\n{'─' * 70}")
            print(f"Challenge #{i + 1}")
            print(f"{'─' * 70}")

            results = []
            for suffix, ciphertext, plaintext in pairs:
                best_key, decrypted_text, score = self.solver.solve(
                    ciphertext,
                    fitness_func=self.solver.fitness_func,
                    num_restarts=25,
                    max_iterations=10000
                )
                # For monoalphabetic substitution, multiple different keys can produce valid English text.
                # We only need to verify that the decrypted text is correct, not the exact key.
                text_match = utils.normalize(decrypted_text) == utils.normalize(plaintext)
                results.append((
                    suffix,
                    text_match,
                    best_key,
                    decrypted_text,
                ))

            success = all(result[1] for result in results)

            if success:
                print(f"✓ [PASS] Challenge #{i + 1}")
                print(f"  Expected Key: {key}")
                print(f"  Found Key:    {results[0][2]}")
                print(f"  Score:        {results[0][2]}")
                passed_count += 1
            else:
                print(f"✗ [FAIL] Challenge #{i + 1}")
                print(f"  Expected Key: {key}")
                for suffix, success, found_key, decrypted_text in results:
                    if not success:
                        print(f"\n  Attempt{suffix or ''}:")
                        print(f"    Found Key: {found_key}")
                        print(f"    Decrypted text (first 200 chars):")
                        text_preview = decrypted_text.replace('\n', ' ')[:200]
                        print(f"    {text_preview}...")
                failed_count += 1

        print("\n" + "=" * 70)
        print("Test Summary")
        print("=" * 70)
        print(f"Passed:  {passed_count}")
        print(f"Failed:  {failed_count}")
        print(f"Skipped: {skipped_count}")
        print(f"Total:   {passed_count + failed_count + skipped_count}")
        print("=" * 70)
        return failed_count == 0

monoalphabetic_solver_test = MonoalphabeticSolverTest()
monoalphabetic_solver_test.run_tests()