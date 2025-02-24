from Crypto.Cipher import AES
import hashlib

def decrypt_file(file_path, key, output_path):
    with open(file_path, 'rb') as file:
        nonce = file.read(16)
        tag = file.read(16)
        ciphertext = file.read()
    
    effective_key = hashlib.sha256(key).digest()
    cipher = AES.new(effective_key, AES.MODE_EAX, nonce=nonce)
    
    try:
        file_data = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        print(f"Verification failed for file {file_path}. The file may be corrupted or the key is incorrect.")
        return
    
    with open(output_path, 'wb') as file:
        file.write(file_data)

def load_key(key_path):
    with open(key_path, 'rb') as key_file:
        key = key_file.read()
    return key