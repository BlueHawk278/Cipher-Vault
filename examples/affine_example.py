from ciphers.affine import AffineCipher

# We create an Affine cipher object with keys a=5 and b=8
# (5 is valid because greatest common divisor of 5 and 26 is 1)
cipher = AffineCipher()

original_message = "This is a secret message!"
print(f"Original:  {original_message}")

# Encrypt the message using: E(x) = (5x + 8) mod 26
encrypted_message = cipher.encrypt(original_message, 5, 8)
print(f"Encrypted: {encrypted_message}")
# Output: Rbgk gk a kieldr rdkkaid!

# Decrypt the message using: D(x) = 21 * (x - 8) mod 26
# (21 is the modular inverse of 5, since (5 * 21) % 26 == 1)
decrypted_message = cipher.decrypt(encrypted_message, 5, 8)
print(f"Decrypted: {decrypted_message}")
# Output: This is a secret message!