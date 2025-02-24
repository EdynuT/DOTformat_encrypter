from Crypto.Cipher import AES
import os

def encrypt_file(file_path, key, output_path):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    
    with open(file_path, 'rb') as file:
        file_data = file.read()

    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    
    with open(output_path, 'wb') as file:
        file.write(nonce + tag + ciphertext)
    
    print(f"Arquivo {file_path} criptografado e salvo como {output_path}")
    return output_path

def save_key(key, key_path):
    with open(key_path, 'wb') as key_file:
        key_file.write(key)
    print(f"Chave de criptografia salva em {key_path}")
