import rsa
import rsa.randnum
import pyAesCrypt


def main():
    #generate shared key
    shared_key = str(rsa.randnum.read_random_bits(128))

    input("Please save your public key (save as public.pem) and hit enter: ")
    
    #encrypt file using shared key
    pyAesCrypt.encryptFile("secret.txt", "protectedsecret.txt.aes", shared_key)
    
    # Load Public Key from file
    with open('public.pem', mode='r') as publicfile:
        keydata = publicfile.read()
        public_key = rsa.PublicKey.load_pkcs1(keydata)

    encrypted_shared_key = rsa.encrypt(bytes(shared_key, 'utf-8'), public_key)
    with open('enc_shared_key.txt', 'wb') as enc_sk:
        enc_sk.write(bytes(encrypted_shared_key))
    
    
if __name__ == '__main__':
    main()