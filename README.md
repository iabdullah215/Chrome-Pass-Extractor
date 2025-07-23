# Chrome Password Extractor

This Python script extracts saved passwords from Google Chrome on Windows and displays them in the terminal.

## Disclaimer

This script is for **educational and ethical** purposes **only**. Unauthorized use to access someone else’s data is illegal and unethical. Use responsibly and with consent.

## Features

- Extracts saved passwords from Chrome
- Decrypts using Chrome's encrypted key and AES
- Displays extracted credentials in the terminal


## 🔧 Requirements

- Python 3.x  
- Windows OS  
- The following Python modules:
  - `pycryptodome`
  - `pywin32`  

## Install dependencies:

```bash
pip install pycryptodome pywin32
```

## Usage

```
python chrome_passwords.py
```

No arguments are needed — passwords will be printed directly in the terminal.

## Output

Each entry will include:
- Website URL
- Username
- Password

## Example:

```console
URL: https://example.com
Username: johndoe
Password: mysecurepassword123
```

## How It Works

- Retrieves Chrome’s local encryption key
- Decrypts passwords from the "Login Data" SQLite database
- Displays decrypted credentials to terminal
