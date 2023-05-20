import rsa
import pyAesCrypt

def generate_keys():
    return rsa.newkeys(1024, poolsize=2)

def main():
    receiver_pub, receiver_priv = generate_keys()

    # Save Public Key into a file
    with open('public.pem', mode='wb') as publicfile:
        publicfile.write(receiver_pub.save_pkcs1("PEM"))

    input("Save shared key encrypted file. Then hit enter: ") #send public.pem

    with open('enc_shared_key.txt', mode='rb') as enc_shared_key:
        encrypted_shared_key = enc_shared_key.read()
        print(encrypted_shared_key)
        shared_key = rsa.decrypt(encrypted_shared_key, receiver_priv).decode('utf-8')

    pyAesCrypt.decryptFile("protectedsecret.txt.aes", "secret.txt", shared_key)


if __name__ == '__main__':
    main()
