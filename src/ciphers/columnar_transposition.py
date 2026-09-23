import math

class ColumnarTransposition:

    def encrypt(self, cipher_text: str, key: str) -> str:
        num_cols = len(key)

        remainder = len(cipher_text) % num_cols
        if remainder != 0:
            padding_needed = num_cols - remainder
            cipher_text += "_" * padding_needed

        num_rows = math.ceil(len(cipher_text) / num_cols)

        grid = []
        for i in range(num_rows):
            row = cipher_text[i * num_cols:(i + 1) * num_cols]
            grid.append(row)

        col_order = self.get_column_order(key)

        ciphertext_chunks = []
        for col_idx in col_order:
            for row in grid:
                ciphertext_chunks.append(row[col_idx])

        return "".join(ciphertext_chunks)

    def decrypt(self, cipher_text: str, key: str) -> str:
        num_cols = len(key)
        num_rows = len(cipher_text) // len(key)

        col_order = self.get_column_order(key)

        grid = [[""] * num_cols for _ in range(num_rows)]

        text_index = 0
        for col_idx in col_order:
            for r in range(num_rows):
                grid[r][col_idx] = cipher_text[text_index]
                text_index += 1

        plaintext_chunks = []
        for row in grid:
            plaintext_chunks.append("".join(row))

        return "".join(plaintext_chunks).rstrip("_")

    def get_column_order(self, key: str) -> list[int]:
        return sorted(range(len(key)), key=lambda i: key[i].lower())