import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import shutil
import secrets
from scripts.encrypt import encrypt_file, save_key
from scripts.decrypt import decrypt_file, load_key
from utils.file_transform import combine_dotf_files, split_dotf_file

encryption_key = None
backup_key_path = None

def get_desktop_path():
    return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

def get_program_path():
    return os.path.dirname(os.path.abspath(__file__))

def get_keys_path():
    keys_path = os.path.join(get_program_path(), 'keys')
    os.makedirs(keys_path, exist_ok=True)
    return keys_path

def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    return file_paths

def select_directory():
    directory = filedialog.askdirectory()
    return directory

def choose_files_or_folder():
    choice_window = tk.Toplevel(root)
    choice_window.title("Escolha")

    def select_files_action():
        choice_window.destroy()
        encrypt_and_transform(select_files())

    def select_folder_action():
        choice_window.destroy()
        folder_path = select_directory()
        if not folder_path:
            return
        file_paths = []
        for root_dir, _, files in os.walk(folder_path):
            for file in files:
                file_paths.append(os.path.join(root_dir, file))
        encrypt_and_transform(file_paths, folder_path)

    tk.Label(choice_window, text="Deseja selecionar arquivos individuais ou uma pasta inteira?").pack(pady=10)
    tk.Button(choice_window, text="Selecionar Arquivos Individuais", command=select_files_action).pack(pady=5)
    tk.Button(choice_window, text="Selecionar Pasta Inteira", command=select_folder_action).pack(pady=5)

def encrypt_and_transform(file_paths, base_folder=None):
    global encryption_key, backup_key_path
    if not file_paths:
        return

    output_directory = get_desktop_path()
    output_folder_name = "encrypted_files"
    output_folder_path = os.path.join(output_directory, output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)

    progress_bar['maximum'] = len(file_paths)

    encryption_key = os.urandom(16)
    key_name = secrets.token_hex(32)
    key_path = os.path.join(output_folder_path, f'encryption_key_{key_name}.key')
    save_key(encryption_key, key_path)

    keys_backup_path = get_keys_path()
    backup_key_path = os.path.join(keys_backup_path, f'encryption_key_{key_name}.key')
    save_key(encryption_key, backup_key_path)

    for i, file_path in enumerate(file_paths):
        if base_folder:
            file_name = os.path.relpath(file_path, base_folder)
        else:
            file_name = os.path.basename(file_path)
        encrypted_path = os.path.join(output_folder_path, f'{file_name}.dotf')
        os.makedirs(os.path.dirname(encrypted_path), exist_ok=True)
        encrypt_file(file_path, encryption_key, encrypted_path)

        progress_bar['value'] = i + 1
        root.update_idletasks()

    print(f"Todos os arquivos foram criptografados e salvos na pasta {output_folder_path}")

def decrypt_file_action():
    global encryption_key, backup_key_path
    folder_path = select_directory()
    if not folder_path:
        return

    output_directory = get_desktop_path()
    output_folder_name = "decrypted_files"
    output_folder_path = os.path.join(output_directory, output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)

    key_files = [f for f in os.listdir(folder_path) if f.startswith("encryption_key_") and f.endswith(".key")]
    if not key_files:
        keys_backup_path = get_keys_path()
        key_files = [f for f in os.listdir(keys_backup_path) if f.startswith("encryption_key_") and f.endswith(".key")]
        if not key_files:
            print(f"Chave de criptografia não encontrada na pasta {folder_path} ou na pasta de backup {keys_backup_path}.")
            return
        key_path = os.path.join(keys_backup_path, key_files[0])
    else:
        key_path = os.path.join(folder_path, key_files[0])
    
    encryption_key = load_key(key_path)

    files_to_process = []
    for root_dir, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.dotf'):
                files_to_process.append(os.path.join(root_dir, file))
    progress_bar['maximum'] = len(files_to_process)

    for i, file_path in enumerate(files_to_process):
        file_name = os.path.relpath(file_path, folder_path).replace('.dotf', '')
        decrypted_path = os.path.join(output_folder_path, file_name)
        os.makedirs(os.path.dirname(decrypted_path), exist_ok=True)
        try:
            decrypt_file(file_path, encryption_key, decrypted_path)
            os.remove(file_path)
        except ValueError as e:
            print(f"Erro ao descriptografar {file_path}: {e}")

        progress_bar['value'] = i + 1
        root.update_idletasks()

    try:
        shutil.rmtree(folder_path)
        print(f"Pasta {folder_path} apagada.")
    except Exception as e:
        print(f"Erro ao apagar a pasta {folder_path}: {e}")

    try:
        os.remove(backup_key_path)
        print(f"Cópia da chave {backup_key_path} apagada.")
    except Exception as e:
        print(f"Erro ao apagar a cópia da chave {backup_key_path}: {e}")

    print(f"Todos os arquivos foram descriptografados e salvos na pasta {output_folder_path}")

root = tk.Tk()
root.title("DOTformat Encrypter")

encrypt_button = tk.Button(root, text="Criptografar Arquivo", command=choose_files_or_folder)
encrypt_button.pack(pady=10)

decrypt_button = tk.Button(root, text="Descriptografar Arquivo", command=decrypt_file_action)
decrypt_button.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate')
progress_bar.pack(pady=10, fill='x')

root.mainloop()
