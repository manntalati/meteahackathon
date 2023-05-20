import rsa
import rsa.randnum
import pyAesCrypt
import os
import tkinter as tk
from tkinter import filedialog

global receiver_pub
global receiver_priv


# Receiver
def receiver_keygen():
    receiver_pub, receiver_priv = rsa.newkeys(1024, poolsize=2)
    
    # Save Public Key into a file
    with open(os.path.join(os.path.expanduser('~'), 'Downloads', 'public.pem'), mode='wb') as publicfile:
        publicfile.write(receiver_pub.save_pkcs1("PEM"))
    

def receiver_decryption():
    
    with open(os.path.join(os.path.expanduser('~'), 'Downloads', 'enc_shared_key.txt'), mode='rb') as enc_shared_key:
        encrypted_shared_key = enc_shared_key.read()
        print(encrypted_shared_key)
        shared_key = rsa.decrypt(encrypted_shared_key, receiver_priv).decode('utf-8')


    pyAesCrypt.decryptFile("protectedsecret.txt.aes", "secret.txt", shared_key)


# Sender
def send_file():
    shared_key = str(rsa.randnum.read_random_bits(128))
    
    #encrypt file using shared key

    pyAesCrypt.encryptFile(secretFilePath, secretFilePath+'.aes', shared_key)

    
    public_key = rsa.PublicKey.load_pkcs1(publicKey)

    encrypted_shared_key = rsa.encrypt(bytes(shared_key, 'utf-8'), public_key)
    with open(os.path.join(os.path.expanduser('~'), 'Downloads', 'enc_shared_key.txt'), mode='wb') as enc_sk:
        enc_sk.write(bytes(encrypted_shared_key))


def sender_uploadPubKey():
    pubKeyPath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("PEM Files",
                                                        "*.pem*"),))
    with open(pubKeyPath, 'r') as pubKey:
        global publicKey
        publicKey = pubKey.read()
        print(publicKey)

def sender_uploadSecretFile():
    global secretFilePath
    secretFilePath = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("TXT Files",
                                                        "*.txt*"),))
    print(secretFilePath)

def sender_menu():
    pubKeyButton = tk.Button(text = "Upload Public Key (.pem)", height = 3, width= 10, command = sender_uploadPubKey)
    pubKeyButton.grid(row=1, column=0)

    secretFileButton = tk.Button(text = "Upload Secret File (.txt)", height = 3, width= 10, command = sender_uploadSecretFile)
    secretFileButton.grid(row=1, column=1)

    encryptButton = tk.Button(text = "Encrypt", height = 3, width= 10, command = send_file)
    encryptButton.grid(row=2, column=1)

def receiver_menu():
    label = tk.Label(
    text="Receiver",
    fg="white",
    bg="black",
    width=10,
    height=10
)
    label.grid(row=2, column=1)


def main():
    window = tk.Tk()
    window.geometry("500x500")
    window.title("Secure File Transferer")
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    introLabel = tk.Label(text= "Are you a...", width = 10, height = 3, font = ('Times New Roman', 12))
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