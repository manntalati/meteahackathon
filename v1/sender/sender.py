import rsa
from cryptography.fernet import Fernet


def main():
    shared_key = Fernet.generate_key() #generate shared key
    print(shared_key)
    symmetric_encrypter = Fernet(shared_key) #create instance variable for shared key through Fernet

    # read secret file
    with open('secret.txt', 'rb') as file:
        secretFile = file.read()

    # Encrypt secret and write to file
    encryptedFile = symmetric_encrypter.encrypt(secretFile)
    with open('protectedsecret.txt', 'w') as enc_file:
        enc_file.write(encryptedFile.decode('utf-8'))

    input("Please save your public key (save as public.pem) and hit enter: ")

    with open('public.pem', mode='r') as publicfile:
        keydata = publicfile.read()
        public_key = rsa.PublicKey.load_pkcs1(keydata)

    encrypted_shared_key = rsa.encrypt(shared_key, public_key)
    #encrypted_shared_key = public_key.encrypt(shared_key)
    with open('enc_shared_key.txt', 'w') as enc_sk:
        enc_sk.write(str(encrypted_shared_key))

    # sender complete
    # add user upload of files and way to send back to reciever


if __name__ == '__main__':
    main()

# with open('private.pem', mode='rb') as privatefile:
#    data = privatefile.read()
# private_key = rsa.PrivateKey.load_pkcs1(data)


#from cryptography.hazmat.backends import default_backend
#from cryptography.hazmat.primitives import serialization, hashes
#from cryptography.hazmat.primitives.asymmetric import padding
#from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Generate a symmetric key
#symmetric_key = b'ThisIsTheSharedKey123'  # Replace with your shared key

# Load the recipient's public key
#with open('recipient_public_key.pem', 'rb') as key_file:
#    recipient_public_key = serialization.load_pem_public_key(
#        key_file.read(),
#        backend=default_backend()
#    )

# Encrypt the shared key with the recipient's public key
#encrypted_shared_key = recipient_public_key.encrypt(
#    symmetric_key,
#    padding.OAEP(
#        mgf=padding.MGF1(algorithm=hashes.SHA256()),
#        algorithm=hashes.SHA256(),
#        label=None
#    )
#)

"""

"""