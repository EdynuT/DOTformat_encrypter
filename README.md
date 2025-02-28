# DOTformat Encrypter

DOTformat Encrypter is a tool for encrypting and decrypting files and folders using the AES algorithm. It allows you to select individual files or entire folders for encryption and decryption, ensuring the security of your data. The system encrypts files using the .dotf format, a proprietary format developed by me, Edynu.

## Version

**Current Version:** 2.0.1

## Changelog

### 2.0.1
- Bug fix where the executable could not find the tkdnd lib

### 2.0.0
- Minor bug fixes in key handling and derivation.
- The 2048-byte key is now processed using SHA‑256 to derive the effective AES key.
- Other stability improvements and corrections.

#### Warning
- Keys generated on older versions won't work in this system version

### 1.1.0
- Added `setup_env.py` script for automatic environment setup.
- Improved project structure and import handling.
- Updated documentation with setup instructions.

### 1.0.0
- Initial release.

## Features

- Encrypt individual files or entire folders.
- Decrypt encrypted files.
- Save a copy of the encryption key in a secure location.
- Maintain directory structure when encrypting folders.

## Requirements

- Python 3.6 or higher, python 3.11.9 is the recommended
- Python libraries:
  - `tkinter`
  - `pycryptodome`
  - `pyinstaller` (to create the executable)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/EdynuT/DOTformat_encrypter.git
   cd DOTformat_encrypter

2. Set Up the Virtual Environment and Install Dependencies: Run the setup_env.py script to create the virtual environment and install dependencies:
    ```sh
    python setup_env.py

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt

## Usage

1. Run the main script:
    ```sh
    python main.py

2. In the graphical interface, you can choose between encrypting individual files or an entire folder:

    1. Click "Encrypt" to select files or a folder for encryption.
    
    2. Click "Decrypt" to select a folder containing encrypted files for decryption.

3. The encrypted files will be saved in the encrypted_files folder on your Desktop. The encryption key will be saved in the same folder, and a copy will be saved in the `keys` folder within the program directory.

### Create Executable

To generate an executable that includes all dependencies (including the tkdnd directory), follow these steps:

1. **Generate the spec file with the additional data directory**

   Use the `--add-data` option to include the `tkdnd` folder:
   
   ```sh
   pyinstaller --onefile --windowed --name DOTformat_encrypter --add-data "venv/Lib/site-packages/tkinterdnd2/tkdnd;tkinterdnd2/tkdnd" main.py

2. **Verify/Edit the Spec File**
    
    Ensure that your DOTformat_encrypter.spec file contains the following entry:

    ```sh
    datas=[('venv/Lib/site-packages/tkinterdnd2/tkdnd', 'tkinterdnd2/tkdnd')]

3. **Build the Executable**

    Run PyInstaller with the spec file:

    ```sh
    pyinstaller DOTformat_encrypter.spec

The executable will be generated in the dist folder under the name DOTformat_encrypter.exe.

## Project Structure

DOTformat_encrypter/
│
├── keys/
├── scripts/
│   ├── encrypt.py
│   └── decrypt.py
├── utils/
│   └── file_transform.py
├── main.py
├── README.md
├── requirements.txt
└── setup_env.py

## Contribution

Contributions are welcome! Feel free to open issues and pull requests for improvements and fixes.

## License

This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

```plaintext
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.
