import json

from utils.utils import normalize
from solvers.caesar_solver import CaesarSolver

class CaesarSolverTest:

    def __init__(self):
        self.caesar_data = self.load_data()
        self.caesar_solver = CaesarSolver()

    def load_data(self):
        try:
            with open('../test_data.json', 'r') as f:
                data = json.load(f)
                return data['caesar']

        except Exception as e:
            print(e)
            return None

    def run_tests(self):
        print("Starting Caesar Cipher Tests")
        passed_count = 0
        failed_count = 0

        for i, challenge in enumerate(self.caesar_data):
            cipher_text = challenge.get("ciphertext")
            plain_text = challenge.get("plaintext")
            key = int(challenge.get("key"))

            top_result = self.caesar_solver.solve(cipher_text, 1)

            success = False
            for shift, score, decoded_text in top_result:
                if shift == key and normalize(decoded_text) == normalize(plain_text):
                    success = True
                    break

            if success:
                print(f"[PASS] Challenge #{i + 1} (Found key {key})")
                passed_count += 1
            else:
                print(f"[FAIL] Challenge #{i + 1}")
                print(f"  Expected Key: {key}")
                print(f"  Top solver picks were: {[r[0] for r in top_result]}")
                failed_count += 1

        print(f"\n--- Test Summary ---")
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")

CaesarSolverTest().run_tests()