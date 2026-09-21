from ciphers.caesar import CaesarCipher

### Basic Caesar Cipher Example

# We create a cipher object with a key of 5
cipher = CaesarCipher()

original_message = "This is a secret message"
print(f"Original:  {original_message}")

# When shifted forward by 5, the original message becomes:
# "Ymnx nx f xjhwjy rjxxflj"
encrypted_message = cipher.encrypt(original_message, 5)
print(f"Encrypted: {encrypted_message}")

# When shifted back by 5, the encrypted message returns to its original form:
# "This is a secret message"
decrypted_message = cipher.decrypt(encrypted_message, 5)
print(f"Decrypted: {decrypted_message}")
