from Crypto.Cipher import AES

def decrypt_file(file_path, key, output_path):
    with open(file_path, 'rb') as file:
        nonce, tag, ciphertext = file.read(16), file.read(16), file.read()

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    
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