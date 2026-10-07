import json
from typing import Any
from utils.utils import normalize
from solvers.affine_solver import AffineSolver

class AffineSolverTest:

    def __init__(self):
        self.affine_data = self.load_data()
        self.affine_solver = AffineSolver()

    def load_data(self) -> Any | None:
        try:
            with open('../test_data.json', 'r') as f:
                data = json.load(f)
                return data['affine']

        except Exception as e:
            print(e)
            return None

    def run_tests(self):
        print("Starting Affine Cipher Tests")
        passed_count = 0
        failed_count = 0

        if not self.affine_data:
            print("No test data available.")
            return

        for i, challenge in enumerate(self.affine_data):
            cipher_text = challenge.get("ciphertext")
            plain_text = challenge.get("plaintext")
            key = challenge.get("key")

            top_result = self.affine_solver.solve(cipher_text, 1)

            success = False
            for a, b, score, decoded_text in top_result:
                if a == key["a"] and b == key["b"] and normalize(decoded_text) == normalize(plain_text):
                    success = True
                    break

            if success:
                print(f"[PASS] Challenge #{i + 1} (Found key {key})")
                passed_count += 1
            else:
                print(f"[FAIL] Challenge #{i + 1}")
                print(f"  Expected Key: {key}")
                print(f"  Top solver picks were: {"a: " + str([r[0] for r in top_result])}, {"b: " + str([r[1] for r in top_result])}")
                failed_count += 1

        print(f"\n--- Test Summary ---")
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")

affine_test = AffineSolverTest()
affine_test.run_tests()