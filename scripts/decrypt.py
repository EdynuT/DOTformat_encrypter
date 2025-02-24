from Crypto.Cipher import AES
<<<<<<< HEAD
import hashlib
=======
import os
>>>>>>> d33347e54785bdf917f3ee1caf18af3b22d1f604

def decrypt_file(file_path, key, output_path):
    with open(file_path, 'rb') as file:
        nonce, tag, ciphertext = file.read(16), file.read(16), file.read()
<<<<<<< HEAD
    
    effective_key = hashlib.sha256(key).digest()
    cipher = AES.new(effective_key, AES.MODE_EAX, nonce=nonce)
    
    try:
        file_data = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        print(f"Verification failed for file {file_path}. The file may be corrupted or the key is incorrect.")
        return
    
    with open(output_path, 'wb') as file:
        file.write(file_data)
=======

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    
    file_data = cipher.decrypt_and_verify(ciphertext, tag)
    
    with open(output_path, 'wb') as file:
        file.write(file_data)
    
    print(f"Arquivo {file_path} descriptografado e salvo como {output_path}")
>>>>>>> d33347e54785bdf917f3ee1caf18af3b22d1f604

def load_key(key_path):
    with open(key_path, 'rb') as key_file:
        key = key_file.read()
<<<<<<< HEAD
    return key
=======
    print(f"Chave de criptografia carregada de {key_path}")
    return key
>>>>>>> d33347e54785bdf917f3ee1caf18af3b22d1f604
