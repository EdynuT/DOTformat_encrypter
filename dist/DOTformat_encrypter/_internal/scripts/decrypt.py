from Crypto.Cipher import AES
import os

def decrypt_file(file_path, key, output_path):
    with open(file_path, 'rb') as file:
        nonce, tag, ciphertext = file.read(16), file.read(16), file.read()

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    
    file_data = cipher.decrypt_and_verify(ciphertext, tag)
    
    with open(output_path, 'wb') as file:
        file.write(file_data)
    
    print(f"Arquivo {file_path} descriptografado e salvo como {output_path}")

def load_key(key_path):
    with open(key_path, 'rb') as key_file:
        key = key_file.read()
    print(f"Chave de criptografia carregada de {key_path}")
    return key
