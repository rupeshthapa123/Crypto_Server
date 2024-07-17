# from cryptography.fernet import Fernet
# from base64 import b64decode, b64encode

# def decrypt(encrypted_data, key):
#   iv = b64decode(encrypted_data['iv'])
#   cipher = Fernet(key)
#   decrypted = cipher.decrypt(b64decode(encrypted_data['encrypted']), iv=iv)
#   return decrypted.decode()

# # Example usage
# encrypted_data = {
#   "iv": 'e8347c9fa274e01ee93905d39607fc1e',
#   "encrypted": 'U2FsdGVkX18BpYwZuToHOGjcHWvBQiEwiV8rduN/p1aXuboP1NwodMKQO6xff4j5'
# }
# key = b'your_secret_key'  # Replace with the same key used in JavaScript

# decrypted_message = decrypt(encrypted_data, key)
# print(decrypted_message)