# DOTformat Encrypter

DOTformat Encrypter is a tool for encrypting and decrypting files and folders using the AES algorithm. It allows you to select individual files or entire folders for encryption and decryption, ensuring the security of your data. The system encrypts files using the .dotf format, a proprietary format developed by me, Edynu.

<<<<<<< HEAD
## Version

**Current Version:** 1.1.1

## Changelog

### 1.1.1
- Minor bug fixes in key handling and derivation.
- The 2048-byte key is now processed using SHA‑256 to derive the effective AES key.
- Other stability improvements and corrections.

### 1.1.0
- Added `setup_env.py` script for automatic environment setup.
- Improved project structure and import handling.
- Updated documentation with setup instructions.

### 1.0.0
- Initial release.

=======
>>>>>>> d33347e54785bdf917f3ee1caf18af3b22d1f604
## Features

- Encrypt individual files or entire folders.
- Decrypt encrypted files.
- Save a copy of the encryption key in a secure location.
- Maintain directory structure when encrypting folders.

## Requirements

- Python 3.6 or higher, python 3.11.9 is the recommended
<<<<<<< HEAD
=======
- Python libraries:
  - `tkinter`
  - `pycryptodome`
  - `pyinstaller` (to create the executable)
>>>>>>> d33347e54785bdf917f3ee1caf18af3b22d1f604

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/EdynuT/DOTformat_encrypter.git
   cd DOTformat_encrypter

<<<<<<< HEAD
2. Set Up the Virtual Environment and Install Dependencies: Run the setup_env.py script to create the virtual environment and install dependencies:
    ```sh
    python setup_env.py
=======
2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
>>>>>>> d33347e54785bdf917f3ee1caf18af3b22d1f604

## Usage

1. Run the main script:
    ```sh
    python main.py

2. In the graphical interface, you can choose between encrypting individual files or an entire folder:

<<<<<<< HEAD
    1. Click "Encrypt" to select files or a folder for encryption.
    
    2. Click "Decrypt" to select a folder containing encrypted files for decryption.
=======
    1. Click "Encrypt File" to select files or a folder for encryption.
    
    2. Click "Decrypt File" to select a folder containing encrypted files for decryption.
>>>>>>> d33347e54785bdf917f3ee1caf18af3b22d1f604

3. The encrypted files will be saved in the encrypted_files folder on your Desktop. The encryption key will be saved in the same folder, and a copy will be saved in the `keys` folder within the program directory.

### Create Executable

To create an executable of the program, follow these steps:

1. Create the executable:
    ```sh
    pyinstaller --onefile --windowed --name DOTformat_encrypter main.py

<<<<<<< HEAD
2. The executable will be generated in the `dist/DOTformat_encrypter` folder with the name `DOTformat_encrypter.exe`

## Project Structure

DOTformat_encrypter/
│
├── build/
├── dist/
│   └── DOTformat_encrypter
│       └──internal/
├── keys/
├── scripts/
│   ├── encrypt.py
│   └── decrypt.py
├── utils/
│   └── file_transform.py
├── DOTformat_encrypter.spec
├── main.py
├── README.md
├── requirements.txt
└── setup_env.py
=======
2. The executable will be generated in the `dist` folder with the name `DOTformat_encrypter.exe`

## Project Structure

 DOTformat_encrypter/
 │
 ├── build/
 ├── dist/
 │   └── DOTformat_encrypter
 │       ├──internal/
 │       └──DOTformat_encrypter.exe
 ├── keys/
 ├── scripts/
 │   ├── encrypt.py
 │   └── decrypt.py
 ├── utils/
 │   └── file_transform.py
 ├── venv/
 ├── DOTformat_encrypter.spec
 ├── main.py
 ├── README.md
 └── requirements.txt
>>>>>>> d33347e54785bdf917f3ee1caf18af3b22d1f604

## Contribution

Contributions are welcome! Feel free to open issues and pull requests for improvements and fixes.

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

```plaintext
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
<<<<<<< HEAD
of this license document, but changing it is not allowed.
=======
of this license document, but changing it is not allowed.
>>>>>>> d33347e54785bdf917f3ee1caf18af3b22d1f604
