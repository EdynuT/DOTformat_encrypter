import os
import sys

project_root = os.path.dirname(os.path.abspath(__file__))
venv_path = os.path.join(project_root, 'venv', 'Lib', 'site-packages')
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

import ctypes
import ctypes.wintypes
import secrets
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from scripts.encrypt import encrypt_file, save_key, generate_key
from scripts.decrypt import decrypt_file, load_key
from utils.file_transform import combine_dotf_files, split_dotf_file

encryption_key = None
backup_key_path = None
dropped_paths = []

def get_desktop_path():
    try:
        CSIDL_DESKTOP = 0x0000
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOP, None, 0, buf)
        desktop = buf.value
        if desktop and os.path.exists(desktop):
            return desktop
    except Exception:
        pass
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if os.path.exists(desktop):
        return desktop
    return os.path.dirname(os.path.abspath(__file__))

def get_program_path():
    return os.path.dirname(os.path.abspath(__file__))

def get_keys_path():
    keys_path = os.path.join(get_program_path(), 'keys')
    os.makedirs(keys_path, exist_ok=True)
    return keys_path

def encrypt_files_and_folders(paths):
    if not paths:
        messagebox.showerror("Error", "No files or folders selected for encryption.")
        return
    disable_buttons()
    threading.Thread(target=encrypt_and_transform, args=(paths,)).start()

def decrypt_files_and_folders(paths):
    disable_buttons()
    threading.Thread(target=decrypt_and_transform, args=(paths,)).start()

def encrypt_and_transform(paths):
    global encryption_key, backup_key_path
    output_directory = get_desktop_path()
    output_folder_name = "encrypted_files"
    output_folder_path = os.path.join(output_directory, output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)
    
    status_label.config(text="Mapping files...")
    mapped_files = []
    
    for path in paths:
        if os.path.isfile(path):
            out_file = os.path.join(output_folder_path, os.path.basename(path) + '.dotf')
            mapped_files.append((path, out_file))
        elif os.path.isdir(path):
            base_name = os.path.basename(path.rstrip(os.sep))
            for root_dir, dirs, files in os.walk(path):
                rel_dir = os.path.relpath(root_dir, path)
                target_dir = os.path.join(output_folder_path, base_name, rel_dir)
                os.makedirs(target_dir, exist_ok=True)
                for file in files:
                    source_file = os.path.join(root_dir, file)
                    target_file = os.path.join(target_dir, file + '.dotf')
                    mapped_files.append((source_file, target_file))
    
    mapping_progress['maximum'] = len(mapped_files)
    mapping_progress['value'] = len(mapped_files)
    status_label.config(text="Mapping completed. Starting encryption...")
    root.update_idletasks()
    
    encryption_key = generate_key()
    key_name = secrets.token_hex(32)
    key_path = os.path.join(output_folder_path, f'encryption_key_{key_name}.key')
    save_key(encryption_key, key_path)
    keys_backup_path = get_keys_path()
    backup_key_path = os.path.join(keys_backup_path, f'backup_key_{key_name}.key')
    save_key(encryption_key, backup_key_path)
    
    work_progress['maximum'] = len(mapped_files)
    work_progress['value'] = 0
    status_label.config(text="Encrypting files...")
    for source, target in mapped_files:
        encrypt_file(source, encryption_key, target)
        work_progress['value'] += 1
        progress_percent = (work_progress['value'] / work_progress['maximum']) * 100
        work_label.config(text=f"Encryption: {progress_percent:.2f}%")
        root.update_idletasks()
    
    status_label.config(text="Encryption completed.")
    messagebox.showinfo("Success", "Files encrypted successfully!")
    enable_buttons()

def find_key_in_paths(paths):
    candidate_keys = []
    for path in paths:
        if os.path.isfile(path) and path.endswith('.key'):
            candidate_keys.append(path)
        elif os.path.isdir(path):
            for root_dir, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.key'):
                        candidate_keys.append(os.path.join(root_dir, file))
    return candidate_keys

def find_key_in_keys_folder():
    keys_folder = get_keys_path()
    candidate_keys = []
    for root_dir, dirs, files in os.walk(keys_folder):
        for file in files:
            if file.endswith('.key'):
                candidate_keys.append(os.path.join(root_dir, file))
    return candidate_keys

def decrypt_and_transform(paths):
    import os
    from tkinter import filedialog, messagebox
    import shutil

    file_paths = []
    base_folder = None
    if len(paths) == 1 and os.path.isdir(paths[0]):
        base_folder = os.path.normpath(paths[0])
    for path in paths:
        if os.path.isfile(path) and path.endswith('.dotf'):
            file_paths.append(path)
        elif os.path.isdir(path):
            for root_dir, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.dotf'):
                        file_paths.append(os.path.join(root_dir, file))
    
    if not file_paths:
        messagebox.showerror("Error", "No .dotf files found for decryption.")
        enable_buttons()
        return

    candidate_keys = find_key_in_paths(paths)
    if not candidate_keys:
        candidate_keys = find_key_in_keys_folder()
    
    if len(candidate_keys) == 1:
        decryption_key = load_key(candidate_keys[0])
    else:
        key_path = filedialog.askopenfilename(filetypes=[("Key files", "*.key"), ("All files", "*.*")])
        if not key_path:
            messagebox.showerror("Error", "No encryption key selected.")
            enable_buttons()
            return
        decryption_key = load_key(key_path)
    
    output_directory = get_desktop_path()
    output_folder_name = "decrypted_files"
    output_folder_path = os.path.join(output_directory, output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)
    
    status_label.config(text="Decrypting files...")
    work_progress['maximum'] = len(file_paths)
    work_progress['value'] = 0
    for i, file_path in enumerate(file_paths):
        if base_folder:
            rel_path = os.path.relpath(file_path, base_folder)
            if rel_path.endswith('.dotf'):
                out_rel = rel_path[:-5]
            else:
                out_rel = rel_path
            output_file = os.path.join(output_folder_path, out_rel)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
        else:
            output_file = os.path.join(output_folder_path, os.path.basename(file_path).replace('.dotf', ''))
        decrypt_file(file_path, decryption_key, output_file)
        work_progress['value'] = i + 1
        progress_percent = (work_progress['value'] / work_progress['maximum']) * 100
        work_label.config(text=f"Decryption: {progress_percent:.2f}%")
        root.update_idletasks()
    
    status_label.config(text="Decryption completed.")
    messagebox.showinfo("Success", "Files decrypted successfully!")
    enable_buttons()
    
    encrypted_folder_path = os.path.join(get_desktop_path(), "encrypted_files")
    if os.path.exists(encrypted_folder_path):
        shutil.rmtree(encrypted_folder_path)
    if backup_key_path and os.path.exists(backup_key_path):
        os.remove(backup_key_path)
    
    # Remove the decryption key file after decryption
    for key_path in candidate_keys:
        if os.path.exists(key_path):
            os.remove(key_path)

def on_drop(event):
    global dropped_paths
    dropped_paths = root.tk.splitlist(event.data)
    if not dropped_paths:
        messagebox.showerror("Error", "No files or folders dropped.")
        return
    messagebox.showinfo("Files Dropped", "Files/folders dropped successfully. Now choose an action.")

def encrypt_dropped_files():
    global dropped_paths
    if not dropped_paths:
        messagebox.showerror("Error", "No files or folders dropped for encryption.")
        return
    disable_buttons()
    threading.Thread(target=encrypt_files_and_folders, args=(dropped_paths,)).start()

def decrypt_dropped_files():
    global dropped_paths
    if not dropped_paths:
        messagebox.showerror("Error", "No files or folders dropped for decryption.")
        return
    disable_buttons()
    threading.Thread(target=decrypt_and_transform, args=(dropped_paths,)).start()

def disable_buttons():
    encrypt_button.config(state=tk.DISABLED)
    decrypt_button.config(state=tk.DISABLED)

def enable_buttons():
    encrypt_button.config(state=tk.NORMAL)
    decrypt_button.config(state=tk.NORMAL)

root = TkinterDnD.Tk()
root.title("DOTformat Encrypter")

frame = tk.Frame(root, width=400, height=200, bg='lightgray')
frame.pack(pady=20)
frame.pack_propagate(False)

label = tk.Label(frame, text="Drag and drop files or folders here", bg='lightgray')
label.pack(expand=True)
frame.drop_target_register(DND_FILES)
frame.dnd_bind('<<Drop>>', on_drop)

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_dropped_files)
encrypt_button.pack(pady=10)
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_dropped_files)
decrypt_button.pack(pady=10)

mapping_progress = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=350)
mapping_progress.pack(pady=5)
work_progress = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=350)
work_progress.pack(pady=5)

work_label = tk.Label(root, text="Progress: 0.00%")
work_label.pack(pady=5)
status_label = tk.Label(root, text="")
status_label.pack(pady=5)

root.mainloop()
