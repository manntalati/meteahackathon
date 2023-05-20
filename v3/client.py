import rsa
import rsa.randnum
import pyAesCrypt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def receiver_keygen():
    # Generates the keys required for asymmetric encryption
    global receiver_pub
    global receiver_priv
    receiver_pub, receiver_priv = rsa.newkeys(1024, poolsize=2)
    
    # Save Public Key into a file and sends this file to the user's Downloads folder
    with open(os.path.join(os.path.expanduser('~'), 'Downloads', 'public.pem'), mode='wb') as publicfile:
        publicfile.write(receiver_pub.save_pkcs1("PEM"))

    messagebox.showinfo(title="Public Key Saved", message = "Look in Downloads folder to find public key file: (public.pem). Send this file to the sender")
    
    
# Allows user to upload the Encrypted Secret Key's File path to the application
def receiver_uploadEncryptedSKPath():
    global encryptedSKPath
    encryptedSKPath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text Files",
                                                        "*.txt*"),))

# Allows user to upload the Encrypted Secret File's path to the application
def receiver_uploadSecretFilePath():
    global encryptedSecretFilePath
    encryptedSecretFilePath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("AES Files",
                                                        "*.aes*"),))

#Decrypts encrypted files and sends them to the user's Downloads Folder
def receiver_decryption():
    with open(encryptedSKPath, mode='rb') as enc_shared_key:
        encrypted_shared_key = enc_shared_key.read()
        shared_key = rsa.decrypt(encrypted_shared_key, receiver_priv).decode('utf-8')


    pyAesCrypt.decryptFile(encryptedSecretFilePath, encryptedSecretFilePath[:-4], shared_key)

    messagebox.showinfo(title="File Decrypted", message = "Look in Downloads folder to find the decrypted file")


# Sender
def sender_encrypt_file():
    shared_key = str(rsa.randnum.read_random_bits(128))
    
    #encrypt file using shared key
    pyAesCrypt.encryptFile(secretFilePath, secretFilePath+'.aes', shared_key)

    #pulls public key
    public_key = rsa.PublicKey.load_pkcs1(publicKey)

    #encrypts the shared key 
    encrypted_shared_key = rsa.encrypt(bytes(shared_key, 'utf-8'), public_key)


    with open(os.path.join(os.path.expanduser('~'), 'Downloads', 'enc_shared_key.txt'), mode='wb') as enc_sk:
        enc_sk.write(bytes(encrypted_shared_key))
    
    messagebox.showinfo(title="Files Encrypted", message = "Look in Downloads folder to find the encrypted shared key(*.txt) and file(*.aes). Send these 2 files to the receiver")


def sender_uploadPubKey():
    pubKeyPath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("PEM Files",
                                                        "*.pem*"),))
    with open(pubKeyPath, 'r') as pubKey:
        global publicKey
        publicKey = pubKey.read()

def sender_uploadSecretFile():
    global secretFilePath
    secretFilePath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          )

def sender_menu():
    clear_window()
    
    senderLabel = tk.Label(text= "Sender", width = 10, height = 3, font = ('Arial', 18))
    senderLabel.grid(row = 0, column = 0, sticky = 'n')
    
    pubKeyButton = tk.Button(text = "1. Upload Public Key (.pem)", height = 3, width= 30, command = sender_uploadPubKey)
    pubKeyButton.grid(row=1, column=0)

    secretFileButton = tk.Button(text = "2. Upload Secret File", height = 3, width= 30, command = sender_uploadSecretFile)
    secretFileButton.grid(row=2, column=0)

    encryptButton = tk.Button(text = "3. Encrypt", height = 3, width= 30, command = sender_encrypt_file)
    encryptButton.grid(row=3, column=0)

def receiver_menu():
    clear_window()
    
    receiverLabel = tk.Label(text= "Receiver", width = 10, height = 3, font = ('Arial', 18))
    receiverLabel.grid(row = 0, column = 0, sticky = 'n')

    generatePubKey = tk.Button(text = "1. Generate Public Key", height = 3, width= 30, command = receiver_keygen)
    generatePubKey.grid(row=1, column=0)

    encryptedSKButton = tk.Button(text = "2. Upload Encrypted Shared Key (.txt)", height = 3, width= 30, command = receiver_uploadEncryptedSKPath)
    encryptedSKButton.grid(row=2, column=0)

    encryptedFileButton = tk.Button(text = "3. Upload Encrypted File (.aes)", height = 3, width= 30, command = receiver_uploadSecretFilePath)
    encryptedFileButton.grid(row=3, column=0)

    decryptButton = tk.Button(text = "Decrypt", height = 3, width = 30, command = receiver_decryption)
    decryptButton.grid(row=4, column=0)

# Clear Window
def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


def main():
    global window
    window = tk.Tk()
    window.geometry("500x500")
    window.title("Secure File Transferer")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    introLabel = tk.Label(text= "Are you a...", width = 10, height = 3, font = ('Arial', 14))
    introLabel.grid(row = 0, column = 0, sticky = 'n')
    senderButton = tk.Button(text = "Sender", command = sender_menu, height = 3, width= 10)
    recieverButton = tk.Button(text = "Reciever", command= receiver_menu, height = 3, width= 10)
    senderButton.grid(row=0, column=0, sticky = 'nw')
    recieverButton.grid(row=0, column=0, sticky = 'ne')
    recieverButton.grid_rowconfigure(1, weight=1)
    recieverButton.grid_columnconfigure(1, weight=1)
    senderButton.grid_rowconfigure(1, weight=1)
    senderButton.grid_columnconfigure(1, weight=1)


    window.mainloop()
    
if __name__ == "__main__":
    main()