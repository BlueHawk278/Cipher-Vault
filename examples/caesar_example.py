from src.cipher_toolkit.ciphers.caesar import CaesarCipher

### Basic Caesar Cipher Example

# We create a cipher object with a key of 5
cipher = CaesarCipher(5)

original_message = "This is a secret message"
print(f"Original:  {original_message}")

# When shifted forward by 5, the original message becomes:
# "Ymnx nx f xjhwjy rjxxflj"
encrypted_message = cipher.encrypt(original_message)
print(f"Encrypted: {encrypted_message}")

# When shifted back by 5, the encrypted message returns to its original form:
# "This is a secret message"
decrypted_message = cipher.decrypt(encrypted_message)
print(f"Decrypted: {decrypted_message}")
