import json
from solvers.trithemius_solver import TrithemiusSolver

class TrithemiusSolverTest:

    def __init__(self):
        self.data = self.load_data()
        self.solver = TrithemiusSolver()

    def load_data(self):
        try:
            with open('../test_data.json', 'r') as f:
                data = json.load(f)
                return data['trithemius']

        except Exception as e:
            print(e)
            return None

    def run_tests(self):
        print("Starting Trithemius Cipher Tests")
        passed_count = 0
        failed_count = 0

        for i, challenge in enumerate(self.data):
            ciphertext = challenge.get('ciphertext')
            plaintext = challenge.get('plaintext')

            key = int(challenge.get('key'))

            top_result = self.solver.solve(ciphertext)

            success = False
            for shift, score, decoded_result in top_result:
                if shift == key:
                    success = True
                    break

            if success:
                print(f"[PASS] Challenge #{i + 1} (Found key {key})")
                passed_count += 1
            else:
                print(f"[FAIL] Challenge #{i + 1}")
                print(f"  Expected Key: {key} (type: {type(key)})")
                print(f"  Top solver picks were: {[r[0] for r in top_result]}")
                failed_count += 1

        print(f"\n--- Test Summary ---")
        print(f"Passed: {passed_count}")
        print(f"Failed: {failed_count}")

TrithemiusSolverTest().run_tests()