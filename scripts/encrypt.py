from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt_file(file_path, key, output_path):
    try:
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        
        with open(file_path, 'rb') as file:
            file_data = file.read()

        ciphertext, tag = cipher.encrypt_and_digest(file_data)
        
        with open(output_path, 'wb') as file:
            file.write(nonce + tag + ciphertext)
        
        return output_path
    except Exception as e:
        print(f"Error encrypting file {file_path}: {e}")

def save_key(key, key_path):
    with open(key_path, 'wb') as key_file:
        key_file.write(key)

def generate_key():
    return get_random_bytes(32)