import json
from pathlib import Path
from typing import Any
from solvers.vigenere_solver import VigenereSolver
from utils.utils import normalize

class VigenereSolverTest:

    def __init__(self):
        self.vigenere_data = self.load_data()
        self.vigenere_solver = VigenereSolver()

    def load_data(self) -> Any | None:
        try:
            data_path = Path(__file__).resolve().parents[1] / "test_data.json"
            with data_path.open("r") as f:
                data = json.load(f)
                return data["vigenere"]
        except (OSError, KeyError, json.JSONDecodeError) as error:
            print(error)
            return None

    def run_tests(self) -> bool:
        print("Starting Vigenere Cipher Tests")
        passed_count = 0
        failed_count = 0

        if not self.vigenere_data:
            print("No test data available")
            return False

        for i, challenge in enumerate(self.vigenere_data):
            cipher_text = challenge["ciphertext"]
            plain_text = challenge["plaintext"]
            key = challenge["key"]
            top_result = self.vigenere_solver.solve(cipher_text, top_n=1)

            success = any(
                estimated_key == key
                and normalize(decoded_text) == normalize(plain_text)
                for estimated_key, decoded_text, score in top_result
            )

            if success:
                print(f"[PASS] Challenge #{i + 1} (Found key {key})")
                passed_count += 1
            else:
                print(f"[FAIL] Challenge #{i + 1}")
                print(f"  Expected key: {key}")
                print(f"  Top solver picks were: {[result[0] for result in top_result]}")
                failed_count += 1

        print("\n--- Test Summary ---")
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")
        return failed_count == 0

vigenere_solver_test = VigenereSolverTest()
vigenere_solver_test.run_tests()